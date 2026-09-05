#!/usr/bin/env python3
"""Pruebas del lector de ofertas. No tocan la red: se ejecutan solas.

    python3 pruebas.py

Sirven para comprobar que un cambio en vigilante.py no rompe lo importante:
que avise cuando hay entradas y que NO avise cuando no las hay.
"""

import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("v", Path(__file__).parent / "vigilante.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

CFG = dict(v.POR_DEFECTO)  # 3 entradas, 35 € máximo
fallos: list[str] = []


def check(condicion: bool, mensaje: str) -> None:
    print(("  ok    " if condicion else "  FALLO ") + mensaje)
    if not condicion:
        fallos.append(mensaje)


def avisos(payload: dict, fecha: str = "2026-09-18") -> list[dict]:
    ofertas: list[dict] = []
    v.recorrer_json(payload, ofertas)
    return [o for o in v.deduplicar(ofertas)
            if v.interesa(o, CFG) and v.es_de_la_fecha(o, fecha)]


print("Horas (un timestamp ISO se lee entero, no sus minutos:segundos)")
for txt, esperado in [("2026-09-18T09:30:00", "09:30"), ("2026-09-18T19:00:00", "19:00"),
                      ("2026-09-18T17:15:00", "17:15"), ("09:30", "09:30"),
                      ("a las 9:05 h", "09:05")]:
    check(v.extraer_hora(txt) == esperado, f"{txt!r} -> {v.extraer_hora(txt)}")

print("\nPrecios")
for entrada, esperado in [(2600, 26.0), (3000, 30.0), (26, 26.0), (600, 600.0),
                          ("26,00", 26.0), ("36.00 €", 36.0), (0, None), ("hola", None)]:
    check(v._a_numero(entrada) == esperado, f"{entrada!r} -> {v._a_numero(entrada)}")

print("\nQué avisa y qué calla")
completo = {"data": {"sessions": [
    {"startTime": "2026-09-18T09:30:00", "availability": 12,
     "products": [{"name": "Basílica", "price": 26.0}]},
    {"startTime": "2026-09-18T11:00:00", "availability": 2,
     "products": [{"name": "Basílica + torre", "price": 36.0}]},
    {"startTime": "2026-09-18T17:15:00", "availability": 0,
     "products": [{"name": "Basílica", "price": 26.0}]},
    {"startTime": "2026-09-18T19:00:00", "availability": 5,
     "products": [{"name": "Visita guiada", "price": 3000}]},
    {"startTime": "2026-09-25T10:00:00", "availability": 40,
     "products": [{"name": "Basílica", "price": 26.0}]},
]}}
horas = {o["hora"] for o in avisos(completo)}
check(horas == {"09:30", "19:00"}, f"avisa solo de 09:30 y 19:00 (dio {sorted(horas)})")

check(not avisos({"sessions": [{"time": "2026-09-19T10:00:00", "places": 2,
                                "items": [{"title": "Basílica", "price": 26}]}]}, "2026-09-19"),
      "2 plazas cuando pides 3 -> calla")
check(bool(avisos({"sessions": [{"startTime": "2026-09-18T10:00:00", "available": True,
                                 "products": [{"name": "Basílica", "price": 26}]}]})),
      '"available": true -> avisa')
check(not avisos({"sessions": [{"startTime": "2026-09-18T10:00:00", "available": False,
                                "products": [{"name": "Basílica", "price": 26}]}]}),
      '"available": false -> calla')
check(not avisos({"sessions": [{"startTime": "2026-09-18T10:00:00", "capacity": 500,
                                "available": 0,
                                "products": [{"name": "Basílica", "price": 26}]}]}),
      "aforo total 500 pero 0 libres -> calla")
check(not any(o["tipo"] == "Visita privada" for o in avisos(
      {"sessions": [{"startTime": "2026-09-18T12:00:00", "availability": 8,
                     "products": [{"name": "Basílica", "price": 26},
                                  {"name": "Visita privada", "price": 600}]}]})),
      "la visita de 600 € no hereda el precio de 26 €")

print("\nCartel de agotado")
for t in ["Entradas agotadas", "SOLD OUT", "Sense disponibilitat", "Esgotat",
          "No disponible", "Exhaurit"]:
    check(bool(v.AGOTADO.search(t)), f"reconoce {t!r}")
check(not v.AGOTADO.search("Quedan 4 plazas a las 09:30"), "no confunde disponibilidad")

print("\nRespaldo cuando no hay JSON útil")
check(v.ofertas_del_texto("Horas: 09:30 11:00 — desde 26,00 € por persona")[0]["precio"] == 26.0,
      "saca el precio del texto visible")

print()
if fallos:
    print(f"{len(fallos)} FALLOS:")
    for f in fallos:
        print(f"  · {f}")
    sys.exit(1)
print("Todo correcto.")
