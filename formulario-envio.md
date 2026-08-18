# Formulario de envío — campo a campo

Ajustado a los límites reales del formulario. En el mismo orden en que aparece.

---

## App details · máximo 500

    Shopify no emite facturas españolas: faltan la numeración correlativa por serie, el desglose de IVA por tipo y la distinción entre factura simplificada y completa.

    Emite lo resuelve. Numera sin huecos ni duplicados, calcula el desglose, elige el tipo de factura según el importe y el NIF del cliente, y emite la rectificativa sola cuando devuelves un pedido.

    Cada trimestre descargas el libro registro con bases y cuotas por tipo, listo para tu gestoría. Los datos se alojan en la Unión Europea.

Unos 490 caracteres. Si el contador se pasa, borra la última frase.

He quitado a propósito el párrafo que criticaba a las apps genéricas. Servía como
posicionamiento entre nosotros, pero Shopify desaconseja hablar de la competencia
en la ficha y es un rechazo evitable.

---

## App category details

Categoría ya fijada: *Orders and shipping › Orders › Invoices and receipts*. Correcta.

**Document types:** marca `Facturas`, `Notas de crédito` y `Devoluciones`.

Las notas de crédito son las rectificativas, y devoluciones porque se emiten al
reembolsar.

**Customization:** marca **Not applicable for this app**.

La app deja configurar series y datos fiscales, pero eso es configuración, no
personalización del documento. No ofreces colores, tipografías ni logotipo. Marcar
etiquetas que no cumples es de las cosas que el revisor comprueba.

**File management:** `Automatización de correos electrónicos`.

Añade `descarga masiva` solo si en la lista se refiere a exportar datos: tu libro
registro en CSV encaja. Si alude a descargar muchos PDF de golpe, déjalo.

---

## Languages

`Spanish`. Ya está puesto.

---

## Features · cinco, máximo 80 caracteres cada una

    Numeración correlativa por serie y ejercicio, sin huecos ni duplicados

    Rectificativa automática al reembolsar, con serie propia y referencia

    Desglose de IVA por tipo y elección entre factura simplificada y completa

    Envío de la factura al cliente en PDF con enlace de descarga permanente

    Libro registro trimestral descargable con las cifras del modelo 303

---

## Feature media

Elige **Image**, no Video.

La imagen es 1600×900 y puedes usar la captura del PDF del pedido 1004, el de los
tres tipos de IVA. El vídeo de esta sección es opcional y no compensa el trabajo.

Ojo: **el screencast de más abajo sí es obligatorio**, pero ese es privado para
quien revisa, no sale en la ficha. Son cosas distintas.

---

## Screenshots · mínimo 3, a 1600×900

Con su texto alternativo, máximo 64 caracteres:

| # | Captura | Texto alternativo |
|---|---|---|
| 1 | Pedidos y facturas, con una rectificativa debajo de su factura | `Lista de pedidos con sus facturas y rectificativas emitidas` |
| 2 | El PDF del pedido 1004 | `Factura en PDF con el desglose de IVA por tipo impositivo` |
| 3 | Libro de facturas del trimestre | `Libro registro trimestral con bases y cuotas por tipo de IVA` |
| 4 | Incidencias con el aviso del pedido sin NIF | `Aviso de un pedido que no se puede facturar sin NIF` |
| 5 | Datos fiscales | `Pantalla de datos fiscales de la tienda` |

---

## Support

- **Preferred support channel:** Support email address
- **Support email address:** `soporte@emite.es`
- Portal y teléfono: déjalos vacíos

Antes de poner ese correo, **comprueba que la redirección de DonDominio funciona**:
mándate una prueba. Un correo de soporte que no llega es motivo de rechazo y de
reseñas malas.

---

## Resources

- **Privacy policy URL:** `https://emite.fly.dev/privacidad`
- Developer website, FAQ, Changelog, Tutorial: vacíos

---

## Pricing details

Pulsa **Manage** y crea el plan: `Estándar`, 19 USD al mes, 7 días de prueba.

Descripción del plan:

    Facturas y rectificativas ilimitadas. Numeración por series, desglose de IVA, envío al cliente y libro registro descargable.

**No marques** la casilla de cobrar fuera de la Billing API. Cobras con Shopify App
Pricing.

---

## App card subtitle · máximo 62

    Cumple la normativa española: series, IVA y rectificativas

58 caracteres.

---

## App store search terms · máximo 5, 20 caracteres cada uno

    factura
    facturación
    IVA
    verifactu
    rectificativa

Uno por línea, con el botón Add. Nada de «Shopify» ni nombres de competidores.

---

## Web search content · opcional pero hazlo

**Title tag**, máximo 60:

    Facturas españolas para Shopify con IVA y rectificativas

**Meta description**, máximo 160:

    Emite las facturas de tu tienda Shopify según la normativa española: series correlativas, desglose de IVA, rectificativas automáticas y libro para tu gestoría.

Es gratis y te trae visitas desde Google, no solo desde la App Store.

---

## Install requirements

**Sales channel requirements:** marca **My app doesn't require the Shopify Online
Store or Shopify POS**. Tu app vive en el panel y no toca la plantilla.

**Geographic requirements:** marca estas dos y sé explícito:

- `Merchant's business address must be in a specific country/region` → **España**
- `Merchant must accept specific currencies` → **EUR**

Parece que te cierra mercado y es justo lo contrario: **evita que se instale gente
a quien no le sirve**, que es de donde salen las reseñas de una estrella. Y le
ahorra al revisor la duda de por qué tu app avisa en tiendas estadounidenses.

---

## Contact information

- **Merchant review email:** `soporte@emite.es`
- **App submission email:** `adelinambudau@gmail.com`

Deliberadamente distintos. El segundo es por donde Shopify te escribirá durante la
revisión, con plazos que corren, y ahí quieres tu Gmail de siempre, que sabes que
funciona, no un correo redirigido que puede fallar.

Y añade `noreply@shopify.com` a tus contactos para que no caiga en spam.

---

## App testing information

**Test account:** marca **My app doesn't require an account to use it**.

Es cierto: la autenticación la hace Shopify y no hay usuario ni contraseña propios.

**Screencast URL:** obligatorio. Ver más abajo.

**Testing instructions:** máximo 2800.

    Esta app emite facturas conformes a la normativa española (Real Decreto 1619/2012) para tiendas que venden en España. No necesita cuentas ni servicios externos.

    Cómo probarla:

    1. Instalar la app. La pantalla de bienvenida pide los datos fiscales de la tienda. Son obligatorios: Shopify no almacena el NIF ni el domicilio fiscal del comerciante, y una factura no es válida sin ellos. Puedes usar el NIF de prueba B28451920.

    2. Activar la suscripción desde el aviso superior. Sin ella la app se puede recorrer entera, pero no emitir facturas.

    3. Crear un pedido en la tienda y marcarlo como pagado.

    4. En "Pedidos y facturas", escribir un NIF de cliente (por ejemplo 46825913Y) y pulsar "Emitir factura". Después "Ver PDF".

    5. Reembolsar ese pedido desde Shopify indicando CANTIDAD de artículos, no un importe. En unos segundos aparece sola la factura rectificativa, con serie propia, importes en negativo y referencia a la original.

    6. En "Libro de facturas", descargar el CSV del trimestre.

    Dos aclaraciones:

    Ámbito: la app está pensada para tiendas que facturan en España. Si la tienda de prueba no está configurada con España y euros, la pantalla de inicio lo advierte y explica qué ocurrirá. Es intencionado, no un error.

    Datos de clientes: solo se solicita read_orders. El nombre, el domicilio y el NIF del comprador son contenido obligatorio de una factura completa española. Los datos se alojan en la Unión Europea (Fráncfort) y el correo sale desde un proveedor francés.

---

## Lo único que no te puedo preparar: el screencast

Es obligatorio y hay que grabarlo. Menos de tres minutos, sin música ni ruido, y
mostrando la instalación y las funciones principales.

Guion sugerido, unos dos minutos:

1. Instalar la app y aceptar permisos.
2. Pantalla de bienvenida, rellenar los datos fiscales.
3. Activar la suscripción.
4. Pedidos y facturas: meter un NIF y emitir. Abrir el PDF y detenerse en el
   desglose de IVA.
5. Ir a Shopify, reembolsar una unidad indicando cantidad.
6. Volver a la app y enseñar la rectificativa que ha aparecido sola.
7. Libro de facturas: el resumen del trimestre y la descarga del CSV.

Grábalo con la grabadora de pantalla de Windows (`Win + G`) y súbelo a YouTube
**como no listado**, con los comentarios desactivados. Pega esa dirección en
Screencast URL.

El paso 6 es el que vende. Que se vea que nadie ha pulsado nada.
