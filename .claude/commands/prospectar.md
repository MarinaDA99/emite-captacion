---
description: Prepara los contactos del día para Emite, con mensajes listos para copiar y pegar.
---

Rutina diaria de captación para **Emite** (`emite.es`), app de facturación
española para Shopify.

## Qué hacer

1. Lee `captacion/objetivos.csv`. Separador: punto y coma.

2. Coge los primeros **8 objetivos con estado `pendiente`**, salvo que el usuario
   pida otro número.

   Si quedan menos de 8 pendientes, dilo y propón ampliar la lista buscando
   gestorías o asesorías fiscales especializadas en comercio electrónico. Nunca
   inventes empresas: búscalas y comprueba que existen.

3. Para cada objetivo:
   - Si le falta la web, búscala.
   - Abre su web y quédate con: a qué se dedican exactamente, en qué ciudad
     están, y **la dirección de su formulario de contacto**.
   - Si no encuentras formulario y sí un correo publicado abiertamente en su
     web, anótalo, pero **el formulario siempre es preferible**.

4. Escribe `captacion/mensajes/AAAA-MM-DD.md` con un bloque por objetivo:
   nombre, a qué se dedican en una línea, la dirección exacta donde escribir, y
   el mensaje listo para copiar.

5. Actualiza en el CSV el estado a `preparado` y la fecha en la columna
   `preparado`.

6. Termina con un resumen de una línea: cuántos van, cuántos quedan pendientes.

## Cómo escribir cada mensaje

Personalizado de verdad, no una plantilla con el nombre cambiado. **La primera
frase tiene que demostrar que has mirado quiénes son**: su especialidad, un
sector en el que trabajan, algo concreto de su web.

Estructura, unas 120 palabras:

- Una frase sobre ellos, específica y sin peloteo.
- El problema: Shopify no emite facturas españolas, genera un justificante de
  compra. Sus clientes se lo preguntan.
- El favor antes que la venta: la guía `emite.es/guias/verifactu`, útil tengan o
  no la app.
- Qué es Emite, en una frase.
- Una pregunta fácil de contestar.
- Salida cortés: si no encaja, con decirlo basta.

## Reglas que no se saltan

- **Firma siempre como `Emite`**, nunca con un nombre de persona.
- **No envíes nada.** Solo preparas los mensajes; envía el usuario a mano.
- **No ofrezcas nada a cambio de una reseña**: Shopify lo prohíbe y es motivo de
  retirada de la app.
- **Nada de descuentos ni pruebas ampliadas** salvo que el usuario lo pida.
- Ofrece, eso sí, línea directa con quien desarrolla la app, aparecer como
  agencia recomendada en emite.es, y voz en lo que se construye.
- **Solo empresas con formulario o correo publicado en su propia web.** Nada de
  perfiles personales, ni datos sacados de LinkedIn u otras redes, ni correos
  deducidos a partir de un patrón. En España la LSSI prohíbe la comunicación
  comercial no solicitada, y un formulario de contacto es una invitación expresa
  a escribir; un perfil personal, no.
- Tono: castellano llano, sin jerga de marketing, sin signos de exclamación.
