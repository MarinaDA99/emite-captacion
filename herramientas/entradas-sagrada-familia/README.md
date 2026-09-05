# Vigilante de entradas · Sagrada Família

Mira la tienda **oficial** cada cierto rato y avisa cuando salen plazas que
cumplen tus condiciones. Solo mira y avisa: **no compra, no reserva y no crea
cuentas**. La compra la haces tú.

Configurado de fábrica para: **18 y 19 de septiembre de 2026, 3 entradas, hasta
35 € cada una.**

## Antes de nada: qué es oficial y qué no

La única venta oficial, sin comisiones ni recargos, es:

- **https://tickets.sagradafamilia.org** ← la tienda
- https://sagradafamilia.org ← la web de la basílica

Todo lo demás que aparece arriba en Google (`sagradafamiliatickets.tours`,
`ticketsagradafamilia.com`, `sagradafamilia-tickets.org`, `sagradafamiliatickets.org`…)
son revendedores: mismo asiento, 10-25 € más caro, y si algo sale mal la
basílica no responde por ellos. **Tiqets** y **GetYourGuide** sí son
distribuidores reales y a veces tienen cupo cuando la web oficial está agotada,
pero con recargo.

Nadie que te escriba por redes o Wallapop con entradas "de sobra" es de fiar:
la entrada va con hora asignada y control de acceso.

## Instalación (una vez)

```bash
cd herramientas/entradas-sagrada-familia
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Puesta a punto (una vez)

```bash
python3 vigilante.py --calibrar
```

Se abre un navegador de verdad. Acepta cookies, elige el 18 de septiembre y 3
entradas, y avanza hasta ver las horas (o el cartel de agotado). Vuelve al
terminal y pulsa Intro.

Eso graba en `calibracion.json` **todo lo que pide la web por dentro**, y te dice
cuántas ofertas ha sabido reconocer. Si reconoce cero, pásame ese fichero y ajusto
el lector a los campos reales de la tienda.

> Este paso existe porque el lector automático es genérico: busca en las
> respuestas de la web campos que huelan a precio, plazas, hora y fecha. Funciona
> con la forma habitual de un motor de reservas, pero no está comprobado contra
> la tienda real de la Sagrada Família.

## Vigilar

```bash
source .venv/bin/activate
python3 vigilante.py
```

Déjalo en una pestaña del terminal. Consulta cada 15-25 minutos (con variación
al azar, para no machacar el servidor), entre las 7:00 y las 23:00. Cuando
encuentra algo nuevo que encaja:

- notificación del escritorio con sonido (macOS y Linux),
- campanita del terminal,
- línea en `hallazgos.log`,
- y, si lo configuras, aviso al móvil y correo.

Si en alguna consulta no supiera leer la web, deja la respuesta en
`ultima-respuesta.json` para poder ajustarlo (no pisa `calibracion.json`).

Solo avisa **una vez por oferta**: lo ya visto queda en `estado.json`.

## Ajustes · `config.json`

Se crea solo la primera vez, copiado de `config.ejemplo.json`.

| Opción | Para qué |
|---|---|
| `fechas` | Días que buscas, en formato `AAAA-MM-DD`. |
| `entradas` | Cuántas plazas necesitas juntas. |
| `precio_max` | Tope por entrada, en euros. |
| `intervalo_min_s` / `intervalo_max_s` | Margen de espera entre consultas. El mínimo son 5 minutos. |
| `horas_activas` | `[7, 23]` = de 7:00 a 23:00, hora de Madrid. |
| `ntfy_topic` | Aviso al móvil, gratis y sin cuenta (abajo). |
| `email_*`, `smtp_*` | Aviso por correo. |

### Aviso al móvil

Instala la app **ntfy** (Android/iOS, gratis), suscríbete a un nombre de canal
tuyo y difícil de adivinar, y ponlo en `ntfy_topic`. Ejemplo:
`"ntfy_topic": "sagrada-adelina-7fk39"`. Cualquiera que acierte el nombre puede
leer tus avisos, así que no uses uno obvio.

### Aviso por correo (Gmail)

Necesitas una [contraseña de aplicación](https://myaccount.google.com/apppasswords),
no la de tu cuenta:

```json
"email_a": "tu@gmail.com",
"email_de": "tu@gmail.com",
"smtp_host": "smtp.gmail.com",
"smtp_puerto": 587,
"smtp_usuario": "tu@gmail.com",
"smtp_clave": "la-contraseña-de-aplicación"
```

`config.json` está en el `.gitignore` justamente por esto: no se sube al
repositorio.

## Dejarlo en segundo plano (macOS)

Una comprobación cada 20 minutos sin tener el terminal abierto:

```bash
crontab -e
```

```cron
*/20 7-23 * * *  cd /RUTA/A/herramientas/entradas-sagrada-familia && ./.venv/bin/python vigilante.py --una-vez >> cron.log 2>&1
```

## Comprobar que el lector sigue bien

```bash
python3 pruebas.py
```

No tocan la red. Comprueban lo que de verdad importa: que avise cuando hay
entradas y, sobre todo, que **no** avise cuando no las hay (0 plazas, precio por
encima del tope, otra fecha, aforo total confundido con plazas libres).

## Si no encuentra nada

Es lo más probable al principio: 2026 es el centenario de Gaudí y las fechas de
septiembre se liberaron 60 días antes, en julio. Lo que buscas son
**cancelaciones**, y aparecen a cualquier hora. Por eso el vigilante insiste.

Mientras tanto:

- **Franjas raras.** 9:00 de la mañana y a partir de las 18:00 se agotan las
  últimas. El vigilante las ve todas, pero si miras a mano, empieza por ahí.
- **Visita guiada (30 €).** A veces quedan plazas de guiada cuando la entrada
  general está agotada. Entra dentro de tu tope.
- **Torres (36 €).** Se salen de los 35 € por 1 €. Si te vale, sube
  `precio_max` a 40.
- **Misa internacional, gratis.** Domingos a las 9:00, entrada libre hasta
  completar aforo, sin reserva: se hace cola desde las 8:00. Tus fechas son
  viernes y sábado, pero el **domingo 20** cae justo después. No se puede pasear
  por el templo ni hacer fotos.
