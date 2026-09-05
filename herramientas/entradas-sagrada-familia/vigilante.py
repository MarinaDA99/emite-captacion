#!/usr/bin/env python3
"""Vigilante de entradas de la Sagrada Família.

Consulta la tienda OFICIAL (tickets.sagradafamilia.org) cada cierto rato y avisa
cuando aparecen plazas que cumplen tus condiciones (fecha, precio y número de
entradas). Solo mira y avisa: no compra, no reserva y no crea cuentas.

Uso:
    python3 vigilante.py --calibrar    # una vez, para aprender la web
    python3 vigilante.py               # vigilar en bucle
    python3 vigilante.py --una-vez     # una sola comprobación (para cron)

Requiere:  pip install -r requirements.txt  &&  playwright install chromium
"""

from __future__ import annotations

import argparse
import json
import random
import re
import smtplib
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, date
from email.message import EmailMessage
from pathlib import Path
from zoneinfo import ZoneInfo

AQUI = Path(__file__).resolve().parent
CONFIG = AQUI / "config.json"
ESTADO = AQUI / "estado.json"
REGISTRO = AQUI / "hallazgos.log"
CALIBRACION = AQUI / "calibracion.json"
ULTIMA = AQUI / "ultima-respuesta.json"

MADRID = ZoneInfo("Europe/Madrid")

# La tienda oficial. Cualquier otro dominio es reventa con recargo.
TIENDA = "https://tickets.sagradafamilia.org/es/1-individual"

# Nunca consultamos más seguido que esto, por respeto al servidor.
INTERVALO_MINIMO_S = 300

POR_DEFECTO = {
    "fechas": ["2026-09-18", "2026-09-19"],
    "entradas": 3,
    "precio_max": 35.0,
    "url_tienda": TIENDA,
    "intervalo_min_s": 900,
    "intervalo_max_s": 1500,
    "horas_activas": [7, 23],
    "ntfy_topic": "",
    "email_a": "",
    "email_de": "",
    "smtp_host": "",
    "smtp_puerto": 587,
    "smtp_usuario": "",
    "smtp_clave": "",
}

# Pistas para reconocer campos en JSON que no conocemos de antemano.
CLAVES_PRECIO = ("price", "precio", "preu", "amount", "importe", "tarifa", "pvp")
# Ojo: solo claves que signifiquen "lo que QUEDA". "capacity" o "aforo" son el
# total del recinto y darían disponibilidad donde no la hay.
CLAVES_PLAZAS = (
    "available", "availability", "disponible", "disponibles", "stock", "places",
    "plazas", "seats", "quota", "remaining", "libres", "restantes",
)
CLAVES_HORA = ("hour", "hora", "time", "slot", "franja", "datetime", "start")
CLAVES_FECHA = ("date", "fecha", "dia", "day", "jornada")
AGOTADO = re.compile(
    r"(agotad|sold\s*out|esgotat|exhaurit|no\s+disponib|sin\s+disponibilidad"
    r"|sense\s+disponibilitat|no\s+availab|complet)",
    re.IGNORECASE,
)
# Un timestamp ISO se lee entero: si no, "19:00:00" casaría como "00:00".
RE_ISO = re.compile(r"(\d{4}-\d{2}-\d{2})(?:[T ](\d{2}:\d{2}))?")
RE_HORA = re.compile(r"(?<![\d:])([01]?\d|2[0-3]):([0-5]\d)(?![\d:])")


def extraer_hora(texto: str) -> str | None:
    if (m := RE_ISO.search(texto)) and m.group(2):
        return m.group(2)
    if m := RE_HORA.search(texto):
        return f"{int(m.group(1)):02d}:{m.group(2)}"
    return None


def extraer_fecha(texto: str) -> str | None:
    m = RE_ISO.search(texto)
    return m.group(1) if m else None
RE_PRECIO = re.compile(r"(\d{1,3}(?:[.,]\d{2})?)\s*€")


# --------------------------------------------------------------------------- #
# Configuración y estado
# --------------------------------------------------------------------------- #

def cargar_config() -> dict:
    cfg = dict(POR_DEFECTO)
    if CONFIG.exists():
        try:
            cfg.update(json.loads(CONFIG.read_text(encoding="utf-8")))
        except json.JSONDecodeError as e:
            sys.exit(f"config.json tiene un error de sintaxis: {e}")
    cfg["intervalo_min_s"] = max(INTERVALO_MINIMO_S, int(cfg["intervalo_min_s"]))
    cfg["intervalo_max_s"] = max(cfg["intervalo_min_s"], int(cfg["intervalo_max_s"]))
    return cfg


def cargar_estado() -> set[str]:
    if not ESTADO.exists():
        return set()
    try:
        return set(json.loads(ESTADO.read_text(encoding="utf-8")).get("vistas", []))
    except (json.JSONDecodeError, OSError):
        return set()


def guardar_estado(vistas: set[str]) -> None:
    ESTADO.write_text(
        json.dumps({"vistas": sorted(vistas)}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def log(linea: str) -> None:
    marca = datetime.now(MADRID).strftime("%Y-%m-%d %H:%M")
    print(f"[{marca}] {linea}", flush=True)
    with REGISTRO.open("a", encoding="utf-8") as f:
        f.write(f"[{marca}] {linea}\n")


# --------------------------------------------------------------------------- #
# Extracción de ofertas
# --------------------------------------------------------------------------- #

def _a_numero(v) -> float | None:
    """Convierte 26, '26', '26,00', '26.00 €' o 2600 (céntimos) a euros."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        n = float(v)
    elif isinstance(v, str):
        m = re.search(r"\d{1,6}(?:[.,]\d{1,2})?", v)
        if not m:
            return None
        n = float(m.group(0).replace(",", "."))
    else:
        return None
    # Un "precio" de 2600 casi seguro son céntimos. Por debajo de 1000 no lo
    # tocamos: una visita privada de 600 € no debe convertirse en 6 €.
    if n >= 1000 and n == int(n):
        n = n / 100
    # Hasta 1000 € lo damos por leído: si es caro, lo rechaza el filtro de
    # precio. Descartarlo aquí haría que heredase el precio del padre.
    return n if 0 < n < 1000 else None


def _a_entero(v) -> int | None:
    """Plazas que quedan. None = la web no lo dice (no bloqueamos el aviso)."""
    if isinstance(v, bool):
        # "available": true significa que hay, no que quede exactamente una.
        return None if v else 0
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, str) and v.strip().isdigit():
        return int(v.strip())
    return None


def recorrer_json(dato, salida: list[dict], profundidad: int = 0,
                  contexto: dict | None = None) -> None:
    """Busca, en cualquier JSON, objetos que parezcan una oferta de entrada.

    En los motores de reserva el precio suele estar en el producto (hijo) y la
    hora y las plazas en la sesión (padre), así que heredamos hacia abajo lo que
    encontramos arriba: si no, una franja con 0 plazas parecería disponible.
    """
    contexto = contexto or {}
    if profundidad > 12:
        return
    if isinstance(dato, list):
        for x in dato:
            recorrer_json(x, salida, profundidad + 1, contexto)
        return
    if not isinstance(dato, dict):
        return

    claves = {k.lower(): k for k in dato}
    precio = plazas = hora = None
    for pista in CLAVES_PRECIO:
        for baja, real in claves.items():
            if pista in baja and (p := _a_numero(dato[real])) is not None:
                precio = precio if precio is not None else p
    for pista in CLAVES_PLAZAS:
        for baja, real in claves.items():
            if pista in baja and (n := _a_entero(dato[real])) is not None:
                plazas = n if plazas is None else min(plazas, n)
    fecha = None
    for pista in CLAVES_HORA + CLAVES_FECHA:
        for baja, real in claves.items():
            if pista in baja and isinstance(dato[real], str):
                hora = hora or extraer_hora(dato[real])
                fecha = fecha or extraer_fecha(dato[real])

    etiqueta = ""
    for k in ("name", "nombre", "title", "titulo", "label", "descripcion", "description"):
        if k in claves and isinstance(dato[claves[k]], str):
            etiqueta = dato[claves[k]].strip()[:80]
            break

    # Lo de este nivel manda; lo que falte se hereda del padre.
    hijo = {
        "precio": precio if precio is not None else contexto.get("precio"),
        "plazas": plazas if plazas is not None else contexto.get("plazas"),
        "hora": hora or contexto.get("hora"),
        "fecha": fecha or contexto.get("fecha"),
        "tipo": etiqueta or contexto.get("tipo") or "entrada",
    }

    if precio is not None or plazas is not None:
        salida.append(dict(hijo))

    for v in dato.values():
        recorrer_json(v, salida, profundidad + 1, hijo)


def deduplicar(ofertas: list[dict]) -> list[dict]:
    """Un mismo dato aparece varias veces al heredar; nos quedamos con lo mejor."""
    mejor: dict[tuple, dict] = {}
    for o in ofertas:
        k = (o.get("fecha"), o["hora"], o["tipo"], o["precio"])
        anterior = mejor.get(k)
        if anterior is None:
            mejor[k] = o
        elif anterior["plazas"] is None and o["plazas"] is not None:
            mejor[k] = o
    return list(mejor.values())


def leer_pagina(page, url: str) -> tuple[list[dict], str]:
    """Abre la url, captura las respuestas JSON y devuelve (ofertas, texto)."""
    capturado: list[dict] = []

    def al_responder(resp):
        tipo = (resp.headers or {}).get("content-type", "")
        if "json" not in tipo.lower():
            return
        try:
            capturado.append({"url": resp.url, "cuerpo": resp.json()})
        except Exception:
            pass  # respuesta no parseable: no nos sirve, seguimos

    page.on("response", al_responder)
    page.goto(url, wait_until="networkidle", timeout=60_000)
    page.wait_for_timeout(3_000)
    texto = page.inner_text("body")
    page.remove_listener("response", al_responder)

    ofertas: list[dict] = []
    for item in capturado:
        recorrer_json(item["cuerpo"], ofertas)
    ofertas = deduplicar(ofertas)

    if not ofertas:
        # No hemos sabido leer nada: guardamos la respuesta para poder ajustar el
        # lector. En fichero aparte, para no pisar lo que grabó --calibrar.
        ULTIMA.write_text(
            json.dumps(capturado, indent=2, ensure_ascii=False)[:2_000_000],
            encoding="utf-8",
        )
    return ofertas, texto


def ofertas_del_texto(texto: str) -> list[dict]:
    """Respaldo: si no hubo JSON útil, saca horas y precios del texto visible."""
    horas = RE_HORA.findall(texto)
    precios = [_a_numero(p) for p in RE_PRECIO.findall(texto)]
    precios = [p for p in precios if p]
    if not (horas and precios):
        return []
    return [{"precio": min(precios), "plazas": None, "hora": None,
             "fecha": None, "tipo": "según texto de la web"}]


# --------------------------------------------------------------------------- #
# Filtro y avisos
# --------------------------------------------------------------------------- #

def interesa(oferta: dict, cfg: dict) -> bool:
    if oferta["precio"] is None or oferta["precio"] > cfg["precio_max"]:
        return False
    # Si la web no dice cuántas plazas quedan, avisamos igual: mejor mirar de más.
    if oferta["plazas"] is not None and oferta["plazas"] < cfg["entradas"]:
        return False
    return True


def clave(fecha: str, oferta: dict) -> str:
    return f"{fecha}|{oferta['hora'] or '-'}|{oferta['tipo']}|{oferta['precio']}"


def es_de_la_fecha(oferta: dict, fecha: str) -> bool:
    """Si la web dijo de qué día es la oferta, exigimos que sea el que buscamos."""
    suya = oferta.get("fecha")
    return suya is None or suya == fecha


def avisar(cfg: dict, titulo: str, cuerpo: str) -> None:
    log(f"AVISO · {titulo} · {cuerpo}")
    print("\a", end="", flush=True)  # campanita del terminal

    if sys.platform == "darwin":
        guion = (
            f'display notification {json.dumps(cuerpo)} '
            f'with title {json.dumps(titulo)} sound name "Glass"'
        )
        subprocess.run(["osascript", "-e", guion], check=False)
    elif sys.platform.startswith("linux"):
        subprocess.run(["notify-send", titulo, cuerpo], check=False)

    if cfg.get("ntfy_topic"):
        try:
            req = urllib.request.Request(
                f"https://ntfy.sh/{cfg['ntfy_topic']}",
                data=cuerpo.encode("utf-8"),
                headers={"Title": titulo.encode("ascii", "ignore").decode(),
                         "Priority": "high", "Tags": "tickets"},
            )
            urllib.request.urlopen(req, timeout=15).read()
        except Exception as e:
            log(f"no pude avisar por ntfy: {e}")

    if cfg.get("email_a") and cfg.get("smtp_host"):
        try:
            msg = EmailMessage()
            msg["Subject"] = titulo
            msg["From"] = cfg.get("email_de") or cfg["smtp_usuario"]
            msg["To"] = cfg["email_a"]
            msg.set_content(f"{cuerpo}\n\nComprar en: {cfg['url_tienda']}\n")
            with smtplib.SMTP(cfg["smtp_host"], int(cfg["smtp_puerto"]), timeout=30) as s:
                s.starttls()
                if cfg.get("smtp_usuario"):
                    s.login(cfg["smtp_usuario"], cfg["smtp_clave"])
                s.send_message(msg)
        except Exception as e:
            log(f"no pude enviar el correo: {e}")


# --------------------------------------------------------------------------- #
# Comprobación
# --------------------------------------------------------------------------- #

def comprobar(cfg: dict, vistas: set[str], navegador) -> int:
    """Una pasada por todas las fechas. Devuelve cuántas novedades encontró."""
    nuevas = 0
    contexto = navegador.new_context(locale="es-ES", timezone_id="Europe/Madrid")
    page = contexto.new_page()
    try:
        for fecha in cfg["fechas"]:
            if date.fromisoformat(fecha) < datetime.now(MADRID).date():
                continue
            try:
                ofertas, texto = leer_pagina(page, cfg["url_tienda"])
            except Exception as e:
                log(f"{fecha}: no pude leer la web ({type(e).__name__}: {e})")
                continue

            if not ofertas:
                ofertas = ofertas_del_texto(texto)

            buenas = [o for o in ofertas
                      if interesa(o, cfg) and es_de_la_fecha(o, fecha)]
            if not buenas and AGOTADO.search(texto):
                log(f"{fecha}: agotado")
                continue
            if not buenas:
                log(f"{fecha}: nada dentro de tus condiciones ({len(ofertas)} opciones vistas)")
                continue

            for oferta in sorted(buenas, key=lambda o: o["precio"]):
                k = clave(fecha, oferta)
                if k in vistas:
                    continue
                vistas.add(k)
                nuevas += 1
                hora = f" a las {oferta['hora']}" if oferta["hora"] else ""
                if oferta.get("fecha") is None:
                    hora += " (confirma la fecha al comprar)"
                plazas = f", {oferta['plazas']} plazas" if oferta["plazas"] else ""
                avisar(
                    cfg,
                    f"Sagrada Família · {fecha}",
                    f"{oferta['tipo']}{hora} · {oferta['precio']:.2f} €{plazas}. "
                    f"Compra ya en {cfg['url_tienda']}",
                )
    finally:
        contexto.close()
    return nuevas


def calibrar(cfg: dict) -> None:
    """Abre el navegador para que elijas la fecha a mano y grabar qué pide la web."""
    from playwright.sync_api import sync_playwright

    capturado: list[dict] = []
    print(
        "\nSe abrirá un navegador en la tienda oficial.\n"
        "  1. Acepta las cookies.\n"
        f"  2. Elige el {cfg['fechas'][0]} y {cfg['entradas']} entradas.\n"
        "  3. Llega hasta ver las horas disponibles (o el cartel de agotado).\n"
        "  4. Vuelve aquí y pulsa Intro.\n"
    )
    with sync_playwright() as p:
        nav = p.chromium.launch(headless=False)
        ctx = nav.new_context(locale="es-ES", timezone_id="Europe/Madrid")
        page = ctx.new_page()

        def al_responder(resp):
            if "json" in (resp.headers or {}).get("content-type", "").lower():
                try:
                    capturado.append({"url": resp.url, "cuerpo": resp.json()})
                except Exception:
                    pass

        page.on("response", al_responder)
        page.goto(cfg["url_tienda"], wait_until="networkidle", timeout=60_000)
        input("Pulsa Intro cuando estés viendo la disponibilidad... ")
        page.screenshot(path=str(AQUI / "calibracion.png"), full_page=True)
        ctx.close()
        nav.close()

    CALIBRACION.write_text(
        json.dumps(capturado, indent=2, ensure_ascii=False)[:2_000_000], encoding="utf-8"
    )
    ofertas: list[dict] = []
    for item in capturado:
        recorrer_json(item["cuerpo"], ofertas)
    ofertas = deduplicar(ofertas)
    print(f"\nGrabadas {len(capturado)} respuestas en calibracion.json")
    print(f"Captura de pantalla en calibracion.png")
    print(f"El lector automático reconoció {len(ofertas)} posibles ofertas.")
    for o in ofertas[:10]:
        print(f"   · {o}")
    if not ofertas:
        print(
            "\nNo reconoció ninguna. Pásale calibracion.json a Claude y que ajuste\n"
            "la función recorrer_json() a los campos reales de la web."
        )


# --------------------------------------------------------------------------- #

def main() -> None:
    ap = argparse.ArgumentParser(description="Vigila entradas de la Sagrada Família.")
    ap.add_argument("--calibrar", action="store_true", help="abrir navegador y grabar la web")
    ap.add_argument("--una-vez", action="store_true", help="comprobar una sola vez y salir")
    args = ap.parse_args()

    cfg = cargar_config()
    if not CONFIG.exists():
        CONFIG.write_text(json.dumps(POR_DEFECTO, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"He creado {CONFIG.name}. Revísalo antes de vigilar en serio.\n")

    if args.calibrar:
        calibrar(cfg)
        return

    from playwright.sync_api import sync_playwright

    vistas = cargar_estado()
    log(
        f"Vigilando {', '.join(cfg['fechas'])} · {cfg['entradas']} entradas · "
        f"hasta {cfg['precio_max']:.0f} € cada una"
    )

    with sync_playwright() as p:
        nav = p.chromium.launch(headless=True)
        try:
            while True:
                ahora = datetime.now(MADRID)
                desde, hasta = cfg["horas_activas"]
                if desde <= ahora.hour <= hasta or args.una_vez:
                    try:
                        n = comprobar(cfg, vistas, nav)
                        guardar_estado(vistas)
                        if n:
                            log(f"{n} novedad(es). Corre a comprarlas.")
                    except Exception as e:
                        log(f"fallo en la comprobación ({type(e).__name__}: {e})")
                else:
                    log("fuera de horario, no miro")

                if args.una_vez:
                    return
                espera = random.randint(cfg["intervalo_min_s"], cfg["intervalo_max_s"])
                log(f"siguiente comprobación en {espera // 60} min")
                time.sleep(espera)
        except KeyboardInterrupt:
            log("parado a mano")
        finally:
            nav.close()


if __name__ == "__main__":
    main()
