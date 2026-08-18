# Despliegue en Fly.io — pasos exactos

Todo lo del código ya está hecho: `Dockerfile`, `fly.toml`, `.dockerignore` y el
destino musl de Prisma. Lo que queda son comandos y secretos.

## 1. Instalar flyctl y entrar

    powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

Cierra y abre el terminal. Luego:

    fly auth signup

Pide tarjeta aunque no cobren de entrada: es para evitar abusos.

## 2. Crear la app sin desplegar todavía

Desde la carpeta del proyecto:

    fly launch --no-deploy --copy-config --name emite --region fra

Si `emite` está cogido por otra persona, elige otro nombre y cámbialo también en
`fly.toml`. El nombre determina la dirección `https://<nombre>.fly.dev`.

Di **NO** si ofrece crear una base de datos Postgres: ya tienes Neon.

## 3. Cargar los secretos

Las variables NO van en la imagen. Se inyectan como secretos.

Los valores de Shopify se obtienen con:

    shopify app env show

Luego, en un solo comando (sustituye cada valor):

    fly secrets set SHOPIFY_API_KEY="..." SHOPIFY_API_SECRET="..." SCOPES="write_products,write_metaobjects,write_metaobject_definitions,read_orders" SHOPIFY_APP_URL="https://emite.fly.dev" APP_HANDLE="facturas-es" DATABASE_URL="<cadena agrupada de Neon>" DIRECT_URL="<cadena directa de Neon>" BREVO_API_KEY="<clave>" EMAIL_REMITENTE="facturas@emite.es" EMAIL_NOMBRE_REMITENTE="Emite"

Comprobar que están todos (muestra nombres, no valores):

    fly secrets list

## 4. Desplegar

    fly deploy

El `release_command` aplica las migraciones antes de levantar la máquina. Si
falla, el despliegue se aborta y sigue funcionando la versión anterior.

Ver que responde:

    fly logs

    fly open

## 5. Apuntar Shopify al servidor real

En `shopify.app.facturas-es.toml`:

    application_url = "https://emite.fly.dev"

    [auth]
    redirect_urls = [ "https://emite.fly.dev/auth/callback" ]

    [build]
    automatically_update_urls_on_dev = true

Y desplegar la configuración:

    shopify app deploy --allow-updates

`automatically_update_urls_on_dev` se deja activado: solo actúa al ejecutar
`shopify app dev`, y sin él el desarrollo en local deja de funcionar. El efecto
secundario es que cada vez que trabajes en local hay que volver a lanzar
`shopify app deploy` antes de dar por buena la producción.

## 6. Comprobar en una tienda limpia

Crear una tienda de desarrollo NUEVA e instalar la app desde cero. Es lo que hará
el revisor de Shopify, y es donde salen los fallos que no se ven en la tienda de
siempre.

Repasar:

- Se instala, pide permisos y entra sin errores.
- La primera pantalla es la de bienvenida, no un panel vacío.
- La página de planes se abre y la suscripción de prueba se activa.
- Emitir una factura, verla en PDF, recibir el correo.
- `https://emite.fly.dev/privacidad` carga sin sesión de Shopify.

## Coste

Una máquina compartida de 512 MB siempre encendida: unos 4-5 $/mes. Más Neon
gratis hasta medio giga y Brevo gratis hasta 300 correos al día.

## Cuando el dominio esté listo

    fly certs add app.emite.es

Añadir en DonDominio el registro CNAME que indique Fly, y luego cambiar
`SHOPIFY_APP_URL` y `application_url` a `https://app.emite.es`.

No es urgente: `emite.fly.dev` funciona perfectamente para publicar. El dominio
propio es cosmético para una app embebida, porque el comerciante nunca ve esa
dirección.
