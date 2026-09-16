# Plan de las primeras semanas · desde la aprobación

Aprobada la app el 16 de septiembre de 2026. Este documento cubre de hoy a
mediados de octubre. A partir de ahí manda `plan-hasta-verifactu.md`.

Ritmo: los **dos días intensivos de desarrollo** de siempre, más **30-45 minutos
diarios** de captación. La aprobación no cambia el ritmo, cambia el orden.

---

## De qué se parte hoy

| | |
|---|---|
| Contactados el 21 de agosto | 7 agencias, ninguna respuesta anotada (26 días) |
| Mensajes preparados sin enviar | 24 — 11 agencias y 13 gestorías, escritos el 24, 25 y 26 de agosto |
| Pendientes de verificar | 1 (Bihotz Studio) |
| Descartados con motivo | 11 |
| Rutina diaria automática | sin salida a internet desde el 26 de agosto: 16 sesiones perdidas |

Los mensajes preparados están en `captacion/mensajes/2026-08-24.md`, `-25` y
`-26`. Son el activo más valioso de este momento: veinticuatro cartas escritas,
personalizadas y sin enviar.

**Hay que reescribirles la primera línea antes de mandarlos.** Se escribieron
cuando la app estaba en revisión. Hoy dicen menos de lo que se puede decir: la
app está publicada y se puede instalar.

---

## Las seis cosas que importan, en orden

### 0 · El cobro. Hoy, antes que nada

Según `factura-espana-brief.md`, a fecha de agosto no había alta de autónomo. La
app ya está publicada con Managed Pricing y prueba de 7 días: **el primero que la
instale esta semana entra en cobro la semana que viene.** Esto tiene plazos que
no dependen de ti (cita con el gestor, alta censal, alta en RETA), así que empieza
hoy aunque no haya ni una instalación.

La llamada al gestor sirve para dos cosas a la vez, como dice el calendario: te
resuelve el alta y te valida las reglas de facturación. No son dos llamadas.

Comprueba también en el panel de Shopify que los datos fiscales y de cobro
(paso 24 de la fase D) están completos. Una app publicada que no puede cobrar es
una app publicada que no es un negocio.

### 1 · Las primeras 72 horas de captación

Lo que dice `captacion/calendario.md`, con los nombres concretos:

- **Los 7 del 21 de agosto.** Llevan 26 días sin respuesta. Según `/seguimiento`
  les tocaba un único recordatorio, y la aprobación es la mejor excusa que vas a
  tener para gastarlo: *ya está publicada, aquí está el enlace*. Un recordatorio
  por objetivo, no dos. Fantasticfy, Numéricco, Soy.es, lyra, Moddo, Nitsnets,
  Migraciones.io.
- **Las comunidades.** Los grupos y el foro en español donde llevabas semanas
  leyendo sin vender. Ahora sí toca decirlo, una vez y sin repetirlo.
- **El primer comerciante real.** La tienda de tu pareja, la de un conocido,
  cualquiera que venda de verdad. Un cliente real antes que uno perfecto: la
  primera factura emitida por alguien que no eres tú vale más que las siguientes
  diez conversaciones.

### 2 · El número inicial de serie, antes de escribir a las gestorías

Es el primer punto del bloque 1 de `plan-hasta-verifactu.md`, un día de trabajo,
y ahora mismo **es lo que decide a quién puedes escribir**.

Hoy toda serie empieza en 1. Un cliente nuevo de una agencia que monta una tienda
desde cero no lo nota. Pero el cliente típico de una gestoría ya va por la factura
340 de este ejercicio, y a ese no le puedes pedir que vuelva a empezar en 1: le
rompes la correlatividad del ejercicio.

De ahí la separación de las tandas de abajo: **las 11 agencias pueden salir ya;
las 13 gestorías, después de este día de trabajo.** Escribirle a trece asesorías
fiscales para que descubran solas que la app no admite continuar una numeración
es quemar trece contactos que te costaron tres días preparar.

### 3 · El resto del bloque 1

Captura del NIF en la página de agradecimiento (2 días), logotipo del comerciante
en el PDF (1) y recargo de equivalencia (1). Sin cambios respecto al plan: es lo
que hace que la app sirva a quien ya factura.

El NIF automático es además lo que más soporte te va a ahorrar. Mientras se meta a
mano, cada pedido de más de 400 € sin NIF es una incidencia que alguien tiene que
resolver, y ese alguien al principio eres tú.

### 4 · Las reseñas

La app las pide sola tras tres facturas, pero un mensaje personal convierte mucho
más. En cuanto haya tres comerciantes con facturas emitidas, pídelas a mano, una
a una. Sin ofrecer nada a cambio: Shopify lo prohíbe y es motivo de retirada.

**Nada de anuncios hasta tener cinco reseñas.** Antes de eso cada clic pagado
aterriza en una ficha sin prueba social.

### 5 · Verifactu, a partir de mediados de octubre

El bloque 2 del plan largo (registros, huella encadenada, QR, anulación, pruebas)
sigue donde estaba: octubre. No se adelanta por la aprobación y no se retrasa por
la captación. Si en octubre sigues apagando fuegos de soporte, el problema es que
el bloque 1 no estaba cerrado.

---

## Semana a semana

### Semana 1 · 16 a 20 de septiembre

| Día | Captación (30-45 min) | Desarrollo |
|---|---|---|
| Miércoles 16 | Recordatorio a los 7 del 21 de agosto | Llamada o cita con el gestor. Revisar datos de cobro en el panel |
| Jueves 17 | Publicar en las comunidades donde ya participabas | Vigilar producción: `fly logs --app emite --no-tail` a diario |
| Viernes 18 | Instalar la app en la tienda de un conocido que venda de verdad | — |
| Fin de semana | Nada | Nada |

Regla de la primera semana en producción: **ningún despliegue en viernes.** Si
algo se rompe un sábado, se rompe con un comerciante real dentro.

### Semana 2 · 21 a 27 de septiembre

| | |
|---|---|
| Día intensivo 1 | Número inicial de serie (1 día del bloque 1) |
| Día intensivo 2 | Captura del NIF en la página de agradecimiento, primera mitad |
| Captación | Tanda A: las 11 agencias preparadas, en grupos de 4 o 5 por día, no las once de golpe |
| Cada día | Responder soporte el mismo día. Al principio eso es la mitad del producto |

Antes de enviar cada mensaje: abrir el enlace del formulario y comprobar que
existe. Se escribieron con el buscador, sin poder visitar las webs, y así lo
avisan los propios ficheros de mensajes.

### Semana 3 · 28 de septiembre a 4 de octubre

| | |
|---|---|
| Día intensivo 1 | Terminar la captura del NIF |
| Día intensivo 2 | Logotipo del comerciante en el PDF |
| Captación | Tanda B: las 13 gestorías, ya con la numeración inicial resuelta y contándolo en el mensaje |
| Revisión | Contar respuestas de la tanda A y buscar el patrón, como manda `/seguimiento` |

Para las gestorías, el segundo párrafo cambia: no montan tiendas, llevan la
contabilidad de quien las tiene. Y el enlace que les sirve es la guía de
Verifactu, que es lo que se les viene encima en 2027. Ya está así en los mensajes
preparados; solo hay que añadir que la app ya está publicada.

### Semana 4 · 5 a 11 de octubre

| | |
|---|---|
| Día intensivo 1 | Recargo de equivalencia. Con esto cierra el bloque 1 |
| Día intensivo 2 | Optimizar la ficha con lo aprendido: las palabras que usan los que contestaron |
| Captación | Recordatorio único a la tanda A. Primeras tiendas `myshopify.com`, en tandas pequeñas |
| Reseñas | Si hay tres clientes con facturas emitidas, pedirlas a mano |

Sobre las tiendas sueltas: el calendario ya avisa de que solo valen las que tengan
un canal de contacto que invite explícitamente a propuestas de proveedores, no un
genérico de atención al cliente, y siempre en tandas pequeñas.

### A partir del 12 de octubre

Bloque 2 de `plan-hasta-verifactu.md`. La captación pasa a ser mantenimiento:
recordatorios, comunidades y lo que entre por la ficha.

---

## La rutina diaria automática

Lleva desde el 26 de agosto sin salida a internet. Dieciséis sesiones seguidas
anotando el mismo bloqueo en el CSV. Eso no se arregla solo y no tiene sentido
seguir reintentándolo a diario.

Dos hechos que deciden qué hacer:

- **`/prospectar` necesita internet.** Verificar el formulario de contacto en la
  web propia de cada empresa exige abrirla, y ahí está el bloqueo.
- **`/seguimiento` no lo necesita.** Trabaja sobre `captacion/objetivos.csv`, que
  está en el repositorio.

Mientras haya 24 objetivos preparados sin enviar, prospectar no está en el camino
crítico: hay tres semanas largas de envíos por delante. Lo sensato es apuntar la
tarea diaria a `/seguimiento`, que sí funciona, e intentar `/prospectar` una vez
por semana. Y revisar la política de red del entorno cuando haya un rato: no es
urgente, pero es lo que impide ampliar la lista cuando estos 24 se agoten.

Hay además un detalle recurrente que conviene mirar: varias sesiones han dejado su
commit en un `HEAD` separado sin fusionar a `main`. Se ha corregido cada vez, sin
pérdida de datos, pero conviene que cada sesión parta de `main`.

---

## Qué no hacer estas semanas

- **Anuncios antes de cinco reseñas.**
- **Funciones nuevas que no hayan pedido tres clientes distintos.** La lista de lo
  que falta ya está escrita y priorizada; las peticiones sueltas de un solo
  comerciante van a una lista de espera, no al siguiente día intensivo.
- **Anunciar que cumples Verifactu.** Hasta febrero de 2027 se dice que se está
  construyendo, y la ficha ya lo dice bien: *preparado para Verifactu*.
- **Enviar los 24 mensajes el mismo día.** Si contesta el 20 %, son cinco
  conversaciones simultáneas mientras arreglas la numeración inicial. En tandas.
- **Escribir a correos deducidos.** Sigue mandando la regla de siempre: formulario
  propio, o correo publicado en su propia web. La aprobación de Shopify no cambia
  la LSSI.

---

## Cómo saber si va bien, a 30 días

No por instalaciones. Por esto:

| Señal | Qué significa |
|---|---|
| 3 o más conversaciones reales de las 31 empresas contactadas | El mensaje funciona |
| 0 respuestas de 31 | El problema es el mensaje, no el canal. Reescribirlo antes de mandar ni uno más |
| 1 comerciante emitiendo facturas de verdad cada semana | La app aguanta el mundo real |
| Soporte que se repite siempre por lo mismo | Eso es el siguiente día intensivo, sea lo que sea |
| 5 reseñas | Se abre la puerta a los anuncios |

Un mes después de publicar, con este tamaño de lista, un resultado normal son
unas pocas instalaciones y dos o tres clientes de pago. La ola que importa es la
de julio de 2027, cuando entran los autónomos. Esto es la preparación.
