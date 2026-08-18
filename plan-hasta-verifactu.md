# Plan de desarrollo · agosto 2026 → marzo 2027

Ritmo: **dos días intensivos por semana**, unas 16 horas. De hoy a noviembre hay
unas 10 semanas, es decir **21 días de trabajo**.

---

## Por qué Verifactu no cabe antes de noviembre

La parte difícil no es programar. Es esto:

**El certificado.** Los registros se envían a la AEAT autenticándose con un
certificado digital. ¿De quién? Si es el del comerciante, tu app custodia claves
privadas de terceros, con la responsabilidad legal que eso implica. Si actúas como
apoderado, hay trámite. Esa decisión hay que tomarla, documentarla en la política
de privacidad y sostenerla ante la revisión de Shopify.

**La declaración responsable.** Quien fabrica el software debe declarar
formalmente que cumple el reglamento. Eso es una responsabilidad tuya, no un
`git push`.

**Las pruebas contra la AEAT.** Hay entorno de preproducción, y la integración
siempre tarda más de lo previsto: errores mal documentados, certificados que
caducan, respuestas que no encajan con el manual.

Estimación honesta: **entre 25 y 30 días de trabajo** solo para Verifactu. A dos
días por semana son tres meses largos, y eso contando con que nada se tuerza.

---

## El plan que sí cabe

### Bloque 1 · Cerrar el producto (5 días · hasta mediados de septiembre)

Esto es lo que bloquea vender, y va primero.

| | Días |
|---|---|
| Número inicial de cada serie. Hoy siempre empieza en 1, y eso excluye a todo el que ya factura | 1 |
| Captura del NIF en la página de agradecimiento | 2 |
| Logotipo del comerciante en el PDF. Lo van a pedir todos | 1 |
| Recargo de equivalencia, que en comercio minorista español aparece constantemente | 1 |

Al terminar esto tu app deja de servir solo a quien empieza de cero.

### Bloque 2 · Verifactu, primera mitad (8 días · octubre)

Lo que se puede construir y probar sin depender de la AEAT.

| | Días |
|---|---|
| Registro de facturación por cada factura, con su estructura | 3 |
| Huella encadenada: cada registro enlazado al anterior | 2 |
| Código QR y las menciones obligatorias en el PDF | 1 |
| Registro de anulación | 1 |
| Pruebas automáticas de toda la cadena | 1 |

**A finales de octubre tienes la mitad de Verifactu funcionando.** No puedes
anunciar que cumples, pero sí que estás construyéndolo.

### Bloque 3 · Verifactu, la parte que depende de terceros (12-15 días · noviembre a febrero)

| | Días |
|---|---|
| Decidir y montar el modelo de certificado | 3 |
| Conexión con el servicio de la AEAT | 4 |
| Reintentos, errores, cola de envíos | 3 |
| Pruebas en preproducción | 3-5 |
| Declaración responsable y ajustes legales | 2 |

Aquí es donde los plazos se rompen. **Cuenta con febrero, no con enero.**

---

## Qué recortar para ir más rápido

**Haz solo la modalidad Verifactu, no la de "no verificable".** Son dos formas de
cumplir: enviando los registros a la AEAT al momento, o conservándolos firmados en
el propio sistema con requisitos más estrictos. Hacer solo la primera te ahorra
toda la parte de firma electrónica y de registro de eventos. Es la mitad del
trabajo, y es además la modalidad que la Agencia Tributaria prefiere.

---

## Qué significa llegar en febrero

Te pierdes el pico de enero, el de las sociedades. Pero **el grande es el de julio
de 2027**, cuando entran los autónomos, que son muchísimos más y son exactamente tu
cliente.

Llegar en febrero te deja cinco meses para posicionarte antes de esa ola. Llegar
en enero justo, con la integración recién probada y sin margen, es peor negocio:
un fallo en un envío a la AEAT en enero te cuesta la reputación que necesitas en
julio.

---

## Calendario resumido

| Fecha | Estado |
|---|---|
| Mediados de septiembre | Producto cerrado: numeración inicial, NIF automático, logotipo, recargo |
| Finales de octubre | Registros, huella y QR funcionando |
| Diciembre | Certificado resuelto y primeras pruebas contra la AEAT |
| Febrero 2027 | Verifactu operativo y anunciable |
| Julio 2027 | La ola de los autónomos, contigo ya rodado |
