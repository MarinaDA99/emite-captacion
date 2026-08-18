# Comandos del proyecto Emite

Todos se ejecutan desde `C:\Users\adeli\competitive-sale-app` salvo donde se
indique.

    cd C:\Users\adeli\competitive-sale-app

---

## Día a día

Arrancar el entorno de desarrollo. Deja el proceso corriendo; `p` abre la app,
`q` lo para.

    shopify app dev

---

## Pruebas

Las tres, antes de tocar nada de lógica fiscal y después de cambiarla.

    node scripts/prueba-numeracion.mjs

    node scripts/prueba-calculo.mjs

    node scripts/prueba-pdf.mjs

Enviar un correo de prueba con factura adjunta:

    node scripts/prueba-correo.mjs tu@correo.com

---

## Base de datos

**Parar antes `shopify app dev`**: en Windows, Prisma no puede regenerarse
mientras el servidor tiene abierto el motor.

Crear y aplicar una migración tras cambiar `schema.prisma`:

    npx prisma migrate dev --name descripcion-del-cambio

Si la CLI se queja de que no es interactiva, escribir el SQL a mano en
`prisma/migrations/<fecha>_<nombre>/migration.sql` y luego:

    npx prisma migrate deploy

Regenerar el cliente sin migrar:

    npx prisma generate

Ver los datos en el navegador:

    npx prisma studio

---

## Desplegar

Dos cosas distintas que se confunden con facilidad:

**El código**, a Fly.io. Aplica migraciones solo y levanta la máquina nueva.

    fly deploy --app emite

**La configuración**, a Shopify: permisos, webhooks, URLs. Necesario cada vez que
se toca `shopify.app.facturas-es.toml`.

    shopify app deploy --allow-updates

---

## Fly.io

Estado de las máquinas:

    fly status --app emite

Registros recientes sin quedarse escuchando:

    fly logs --app emite --no-tail

Registros en directo:

    fly logs --app emite

Ver qué secretos hay cargados (nombres, no valores):

    fly secrets list --app emite

Cambiar o añadir un secreto:

    fly secrets set NOMBRE=valor --app emite

Entrar por consola a la máquina:

    fly ssh console --app emite

Reiniciar si algo se queda colgado:

    fly apps restart emite

---

## Comprobar producción desde fuera

    curl -I https://emite.fly.dev/privacidad

---

## Si `fly` no se reconoce

El instalador lo pone en el perfil del usuario. Con la ruta completa funciona
siempre:

    C:\Users\adeli\.fly\bin\flyctl.exe status --app emite
