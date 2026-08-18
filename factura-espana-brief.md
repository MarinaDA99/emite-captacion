# Brief de producto — App de facturación española para Shopify

## Frase única

Mi app hace que una tienda Shopify en España pueda emitir facturas y rectificativas
conformes a la normativa española, sin tener que corregirlas a mano.

## Por qué existe este hueco (evidencia recogida en la App Store, agosto 2026)

- Francia tiene apps de facturación localizadas con tracción (FF: Factures, 40 reseñas ★5,0;
  Regulo, 29 ★5,0). México tiene Facturama (30 ★4,1). Chile tiene Haulmer.
  **España no tiene ninguna app de facturación local con tracción.**
- Lo único orientado a España son tres intentos de Verifactu:
  - Verifactu de Finseed (Barcelona), publicada ago-2025, 12 reseñas, 14,95–99,95 $/mes
  - Verifactu Pro (idnovate, Sant Cugat), publicada jun-2026, 0 reseñas, 9,99 $/mes
  - Comply, 3 reseñas ★3,3, gratis
- Las apps dominantes son generalistas hechas fuera de la UE:
  Vify Order Printer (1.136 reseñas), Avada PDF Invoice (688), Sufio (426).

### Quejas verificadas en reseñas de 1 estrella de esas generalistas

- Sufio (Francia): las facturas no respetan la normativa fiscal de la UE; calcula mal
  cuando hay un descuento aplicado.
- Sufio (Austria): la validación de IVA intracomunitario no funciona de verdad; el
  NIF-IVA se guarda solo como etiqueta y no se expone por la API.
- Sufio (Países Bajos): las notas de abono solo están en el plan Professional.
- Vify (Alemania): una actualización rompió la edición de facturas necesaria para
  cumplir con la fiscalidad alemana.
- Vify (Países Bajos): un solo idioma de factura por tienda.
- Vify / Order Printer (Alemania, Austria): traducciones inservibles.
- Vify (España): problemas de instalación y de cobros duplicados.

### Contexto legal

Real Decreto-ley 15/2025 (BOE 3-dic-2025) aplazó Verifactu un año:
- Sociedades (Impuesto de Sociedades): 1 de enero de 2027
- Autónomos y resto: 1 de julio de 2027
- 2026 es periodo voluntario de pruebas.

Verifactu NO forma parte de la v1. Es la ampliación planificada.

## Alcance de la v1 — siete funciones, ni una más

1. Genera la factura en PDF automáticamente cuando el pedido se marca como pagado.
2. Numeración correlativa por serie y ejercicio, sin huecos ni saltos.
3. Campos obligatorios: NIF de emisor y receptor, domicilio fiscal, fecha de operación,
   base imponible, desglose por tipo de IVA.
4. Descuentos aplicados correctamente sobre la base imponible.
5. Factura simplificada o completa de forma automática, según importe y presencia de NIF.
6. Factura rectificativa automática al producirse una devolución o reembolso en Shopify,
   con serie propia y referencia a la factura original.
7. Envío automático por email al cliente y enlace de descarga.

## Fuera de alcance en la v1 (ampliaciones futuras, no tocar ahora)

- Verifactu y envío a la AEAT
- Recargo de equivalencia
- IVA intracomunitario y validación VIES
- Múltiples idiomas
- TPV / Shopify POS
- Cualquier país que no sea España

Motivo del orden: los puntos 2, 3 y 6 son los cimientos técnicos de una futura app
Verifactu. Al construirlos primero, la ampliación de 2027 parte de un motor ya hecho
y de una base de clientes españoles existente.

## Modelo de negocio

- Un solo plan de pago. Precio de partida sugerido: 19 €/mes.
- Prueba gratuita de 7 días.
- Cobro mediante Managed Pricing de Shopify (Shopify factura y paga).
- Shopify no cobra comisión sobre el primer millón de dólares anuales.

## Estado a 16 de agosto de 2026

Infraestructura terminada. Producto sin empezar.

- Cuenta de Shopify Partners creada. Partner ID 5119927, organización "New Invent".
  Existe una segunda organización, "Mi tienda", creada automáticamente y que NO se usa.
  Trabajar siempre en "New Invent".
- Tienda de desarrollo `Facturas ES Dev` creada, plan Basic, España, EUR, con datos de prueba.
- App creada en Shopify con el nombre `facturas-es`.
- Proyecto local en `C:\Users\adeli\competitive-sale-app`
  (pendiente de renombrar la carpeta a `facturas-es`).
- Plantilla oficial de Shopify con React Router y JavaScript.
  Ya resuelve login, permisos, conexión con Shopify y base de datos (Prisma, migraciones aplicadas).
- La app se instala y se abre embebida dentro del panel de Shopify.
- El botón de demo "generar producto" de la plantilla fallaba con un TypeError opaco
  porque la plantilla no comprobaba `userErrors`. Se añadió la comprobación en
  `app/routes/app._index.jsx`. Es código de demostración destinado a borrarse.

Arrancar el entorno cada día:

    cd C:\Users\adeli\competitive-sale-app
    shopify app dev

Luego pulsar `p` para abrir la vista previa. `q` o Ctrl+C para parar.

## Plan completo hasta tener la app publicada

### Fase A — Infraestructura y diagnóstico (HECHA)
1. Cuenta de Partner, tienda de desarrollo, esqueleto de la app.
2. Permisos, datos protegidos de cliente en desarrollo.
3. Diagnóstico: qué campos da Shopify y cuáles faltan.

### Fase B — El motor de facturas (el producto)
4. Pantalla de ajustes fiscales del emisor: NIF, razón social, domicilio, series.
5. Modelo de datos: tablas de factura y de contador por serie y ejercicio.
6. Numeración correlativa, transaccional, sin huecos ni duplicados.
7. Captura del NIF del receptor: campo en el checkout más alternativa manual
   en la ficha del pedido.
8. Cálculo fiscal: base imponible, desglose por tipo de IVA, descuentos,
   y soporte de precios con y sin IVA incluido.
9. Decisión automática entre factura simplificada y completa.
10. Generación del PDF.
11. Rectificativa automática al reembolsar.
12. Envío por email y enlace de descarga para el cliente.
13. Listado de facturas dentro de la app y exportación para la gestoría.

### Fase C — Robustez (lo que separa un juguete de un producto)
> Aviso surgido al probar la numeración: SQLite solo admite un escritor. Con varias
> conexiones, las transacciones simultáneas se bloquean y agotan el tiempo de espera
> (error P1008). Está resuelto forzando `connection_limit=1`, pero eso serializa la
> emisión de facturas. **El paso 16 no es una mejora opcional: hay que migrar a
> Postgres antes de tener clientes reales.**

14. Webhooks de pedido pagado y de reembolso, con reintentos e idempotencia.
15. Manejo de errores: si una factura falla, el comerciante tiene que enterarse.
16. Migración de SQLite a Postgres.
17. Casos límite: sin dirección, sin NIF, con descuento, varios tipos de IVA,
    reembolso parcial, pedido cancelado, moneda distinta del euro.

### Fase D — Convertirlo en negocio
18. Managed Pricing: un solo plan y prueba gratuita de 7 días.
19. Alojamiento real (Fly.io o Railway) con Postgres (Neon o Supabase).
20. Webhooks obligatorios de RGPD: data_request, customers/redact, shop/redact.
21. Política de privacidad y página de soporte.
22. Ficha de la App Store: nombre, icono, capturas, descripción.
23. Solicitud definitiva de datos protegidos de cliente, nivel 2, con revisión.
24. Datos fiscales y de cobro en Shopify (a nombre del autónomo titular).
25. Envío a revisión, corrección del rechazo casi seguro, reenvío.
26. Publicación.

### Fase E — Después de publicar
27. Optimización de la ficha para la búsqueda de la App Store.
28. Soporte y respuesta a todas las reseñas.
29. Funciones nuevas solo cuando las pidan tres clientes distintos.
30. Módulo Verifactu antes de enero de 2027.
31. Ampliaciones: recargo de equivalencia, IVA intracomunitario con VIES, idiomas.

Los pasos 6, 7 y 11 son los difíciles. Los pasos 18 a 26 son burocracia sin
dificultad técnica pero con esperas.

## Próximos pasos

Hechos los pasos 4 y 6 del plan:

- `app/fiscal/nif.js` — validación real de NIF, NIE y CIF con carácter de control.
  Se reutilizará para el NIF del receptor.
- `app/routes/app.ajustes.jsx` — pantalla de datos fiscales del emisor y series.
- `app/fiscal/numeracion.server.js` — emisión y numeración correlativa, con
  idempotencia por `origen` y serie propia para rectificativas.
- `scripts/prueba-numeracion.mjs` — 9 comprobaciones, todas en verde.
  Ejecutar con `node scripts/prueba-numeracion.mjs` tras cada cambio del motor.

Hechos también los pasos 7 (parcial), 8 y 9:

- `app/routes/app.pedidos.jsx` — lista de pedidos con entrada manual del NIF.
- `app/fiscal/calculo.js` — base imponible, desglose por tipo, envío, decisión
  entre simplificada y completa, y cuadre contra el total cobrado por Shopify.
- `scripts/prueba-calculo.mjs` — 24 comprobaciones, todas en verde.

### Decisiones de diseño que conviene no revertir

**No recalculamos el IVA.** Se toman los importes que Shopify ya calculó y que el
cliente pagó, y se reagrupan como exige la factura española. Recalcular arriesga
diferencias de céntimos entre la factura y el cobro.

**El NIF del receptor no se escribe en Shopify**, se guarda en nuestra base de
datos. Evita pedir permiso de escritura sobre pedidos y otra revisión de datos
protegidos.

**El checkout está cerrado en plan Basic.** Las extensiones de UI en los pasos de
información, envío y pago son exclusivas de Shopify Plus. Como los clientes objetivo
están en Basic, el NIF se captura por tres vías que sí funcionan en todos los planes:
bloque en la página del carrito, extensión en la página de agradecimiento tras la
compra, y entrada manual del comerciante. Las tres escriben en `DatosReceptor`.

**Dinero en coma flotante.** Todos los importes se redondean a dos decimales en cada
paso, así que las salidas son correctas. Si alguna vez aparece descuadre, la solución
es pasar a céntimos enteros. Está controlado, pero es la primera sospecha ante
cualquier diferencia de un céntimo.

Hecho también el paso 10:

- `app/fiscal/pdf.server.js` — PDF con pdfkit, sin navegador sin ventana.
- `app/fiscal/emision.server.js` — une pedido, cálculo y numeración. Incluye
  `shippingLines`, que era el pendiente anterior.
- `app/routes/app.factura.$id.pdf.jsx` — sirve el PDF, siempre filtrando por tienda.
- `scripts/prueba-pdf.mjs` — 12 comprobaciones y facturas de ejemplo en `ejemplos/`.

**Datos congelados, aspecto no.** La copia guardada en `Factura.documento` fija
importes, NIF y fechas. El PDF se dibuja al pedirlo, así que arreglar la maquetación
corrige también las facturas ya emitidas, sin reemitir nada.

Lecciones que costaron intentos y conviene recordar:
- pdfkit guarda el texto en hexadecimal y parte las palabras en fragmentos para
  ajustar el espaciado. Buscar texto plano dentro del PDF no funciona.
- Colocar el pie a una altura fija desbordaba la página por décimas de punto. Hay
  que medir con `heightOfString` y dejar holgura.
- Dos veces seguidas el fallo estaba en la prueba, no en el código. Antes de tocar
  código que funciona, comprobar que la medición es correcta.

Hechos los pasos 11, 12 y 14. Fase B cerrada salvo la captura automática del NIF
y el listado de facturas para la gestoría.

- `app/fiscal/incidencias.server.js` + `app/routes/app.incidencias.jsx` — registro
  visible de lo que falla cuando la app trabaja sola.
- `app/fiscal/rectificativa.server.js` + `webhooks.refunds.create.jsx` — rectificativa
  automática al reembolsar.
- `app/fiscal/email.server.js` — envío con proveedor intercambiable.
- `app/routes/factura.$token.jsx` — descarga pública para el comprador.
- `webhooks.orders.paid.jsx` — emisión automática, desactivada por defecto.
- `scripts/rellenar-tokens.mjs` — asigna enlace a facturas antiguas.

### Reglas de los webhooks, aprendidas aquí

**Responder siempre 200.** Si devuelves error, Shopify reintenta durante días y
acaba desactivando la suscripción. Los problemas van a Incidencias, no a Shopify.

**Dentro de la petición, solo lo crítico.** Emitir sí; enviar el correo no, porque
depende de un servicio ajeno. El envío se lanza sin esperar y sus fallos se
registran. Esto **solo funciona con un servidor siempre encendido** (Fly.io,
Railway). Si algún día se migra a un alojamiento que apaga el proceso al responder,
harán falta colas de trabajo.

**La clave de idempotencia es el hecho, no el pedido.** Un pedido tiene una factura
pero puede tener varias rectificativas, una por devolución parcial.

**Emisión automática desactivada por defecto.** Una factura emitida no se modifica,
solo se rectifica. Si el cliente pide el NIF después de comprar, la emisión
inmediata genera simplificadas que luego hay que rectificar una a una.

### Migraciones cuando la CLI no es interactiva

`prisma migrate dev` pide confirmación si detecta avisos (por ejemplo al añadir un
índice único) y falla en terminal no interactivo. La salida es escribir el SQL a
mano en `prisma/migrations/<fecha>_<nombre>/migration.sql` y aplicar con
`prisma migrate deploy`.

En Windows, `prisma generate` falla con EPERM si `shopify app dev` está corriendo:
hay que parar el servidor antes de cada migración.

### Paso 16 HECHO: Postgres en Neon (Frankfurt)

La base de datos vive en `eu-central-1`. La región importa por dos razones: los
datos personales de compradores españoles no deben salir de la UE (lo revisa
Shopify al pedir el nivel 2 de datos protegidos), y el servidor estará en Europa.

**Fallo de concurrencia descubierto al cambiar.** El `upsert` de Prisma sobre el
contador de serie no es atómico: consulta y luego inserta. Con peticiones
simultáneas, todas ven que el contador no existe y todas intentan crearlo, y
saltan violaciones de clave única. SQLite lo ocultaba porque serializaba todo.
Resuelto con una única instrucción `INSERT ... ON CONFLICT DO UPDATE` en
`numeracion.server.js`. **No usar `upsert` para contadores.**

Las migraciones de SQLite están archivadas en `prisma/migraciones-sqlite-antiguas`
y `prisma/dev.sqlite` conserva los datos de prueba antiguos. Se pueden borrar.

### Paso 17: casos límite resueltos

**Dos fechas, no una.** La numeración debe ser correlativa en el tiempo. Si se usa
la fecha del pedido como fecha de la factura, facturar hoy una venta antigua produce
una factura con número alto y fecha vieja, que es ilegal. Ahora:
- `fecha` = fecha de expedición, siempre el momento de emitir.
- `documento.fechaOperacion` = cuándo ocurrió la venta.
- El PDF muestra la segunda solo cuando difiere de la primera, como exige la norma.

**Divisa distinta del euro.** La cuota de IVA debe expresarse en euros. Si el pedido
viene en otra moneda se emite igual pero con aviso: hay que añadir el contravalor y
el tipo de cambio a mano.

**NIF inválido.** Un NIF llegado del carrito puede no ser válido. Se comprueba antes
de usarlo; si no lo es se descarta y la factura sale simplificada con un aviso.
Emitir una completa con un identificador fiscal falso es peor que no emitirla.

**Sin domicilio fiscal.** Una factura completa debe incluir la dirección del
destinatario. Si falta, no se emite y se explica qué corregir.

### Procedimiento original del cambio (referencia)

Elegido Neon en lugar de Supabase: solo hace falta Postgres, y Supabase arrastra
autenticación, almacenamiento y tiempo real que no se usan. El plan gratuito de
Supabase además pausa la base de datos tras días sin actividad.

Coste: gratis hasta medio giga, luego unos 19 $/mes. Sumado al alojamiento, la
factura mensual con clientes rondará los 25 €.

Ya preparado: la cadena de conexión vive en `.env` como `DATABASE_URL`, no en el
esquema, y `app/db.server.js` la pasa explícitamente con un valor de respaldo por
si la CLI de Shopify no traslada la variable al proceso.

Procedimiento cuando exista la cuenta:

1. En Neon, crear proyecto y copiar **las dos** cadenas de conexión: la agrupada
   (pooled) y la directa. Prisma necesita la directa para migrar y la agrupada
   para funcionar.

2. En `.env`:

       DATABASE_URL="<cadena agrupada>?sslmode=require"
       DIRECT_URL="<cadena directa>?sslmode=require"

   Sin `connection_limit=1`: eso era una limitación de SQLite.

3. En `prisma/schema.prisma`, en el bloque `datasource`:

       provider  = "postgresql"
       url       = env("DATABASE_URL")
       directUrl = env("DIRECT_URL")

4. **Borrar la carpeta `prisma/migrations` entera.** El SQL de las migraciones es
   específico de SQLite y no vale para Postgres. No hay datos de producción que
   perder, solo las facturas de prueba.

5. Crear la migración inicial:

       npx prisma migrate dev --name inicial

6. Volver a rellenar los datos fiscales de la tienda desde la app y pasar los tres
   guiones de prueba.

7. Bajar los márgenes de la transacción en `numeracion.server.js` de 30000 a unos
   5000 ms: con Postgres las transacciones son concurrentes de verdad.

### Siguiente

Fase C: paso 17 (casos límite). El 15 quedó cubierto con Incidencias.
Después la fase D, que es sobre todo burocracia.

## Hallazgo verificado: qué NO da Shopify

Comprobado el 16 de agosto de 2026 contra un pedido real, con la página de
diagnóstico `app/routes/app.factura-datos.jsx`.

Shopify SÍ da: nombre del receptor, dirección de facturación, fecha de operación,
base imponible, descuentos, total, líneas de pedido, y el email en el propio pedido
(sin necesidad del permiso `read_customers`).

Shopify NO da, y por tanto la app tiene que recogerlo:

1. **NIF, razón social y domicilio fiscal del EMISOR.** No existe en Shopify.
   Solución: pantalla de ajustes dentro de la app.
2. **NIF del RECEPTOR.** No existe en el cliente, ni en el pedido, ni en la dirección.
   Solución: campo en el checkout o en la ficha del pedido, leído después desde
   `order.customAttributes`.
3. **Número de factura.** El `order.name` (#1001) es el número de pedido de Shopify
   y no sirve como número de factura.

Esto es el corazón del producto. Las apps generalistas se limitan a imprimir lo que
Shopify les da, y por eso los comerciantes españoles corrigen facturas a mano.

Nota de configuración: la tienda de pruebas debe tener España al 21% en Impuestos y
aranceles, y precios CON IVA incluido, que es lo normal en venta a particulares en
España. La app tendrá que soportar ambos modos. Las tarjetas de regalo están exentas
de IVA y no sirven para probar el desglose.

## Requisito de lanzamiento: datos protegidos de clientes

Shopify clasifica los pedidos como datos personales protegidos. No basta con el
permiso `read_orders`: hay que declarar el uso en el panel, apartado "API access
requests".

- Nivel 1: datos de cliente sin nombre, dirección, email ni teléfono.
- Nivel 2: incluye esos cuatro campos. Requiere revisión de protección de datos.

Esta app necesita **nivel 2**, porque una factura completa española exige nombre y
domicilio fiscal del receptor. Se piden solo nombre, dirección y email; el teléfono
NO se pide, porque Shopify exige pedir el mínimo imprescindible y no hace falta.

En desarrollo el acceso se concede automáticamente al rellenar la declaración.
Para publicar en la App Store hay revisión de Shopify. **Es un bloqueante de
lanzamiento, no un trámite**: conviene tener la declaración bien escrita desde ya.

## Situación fiscal del desarrollador

No es autónomo ni tiene empresa a fecha de agosto de 2026. No hace falta para
desarrollar, probar ni preparar la app. Sí hace falta resolverlo antes de activar
el cobro y recibir pagos de Shopify. Consultar con un gestor cuando se acerque
el lanzamiento; el mismo gestor sirve como asesor de dominio y primer validador
de las reglas de facturación.

## Posicionamiento

No es "una app de facturas". Es "la app de facturas para España".
La primera línea de la ficha debe nombrar el problema del comerciante español,
no la lista de funciones.
