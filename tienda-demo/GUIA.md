# Montar la tienda de demostración

Tienda: `facturas-es-review-test`. Objetivo: que las capturas de la ficha parezcan
una tienda real, no un entorno de pruebas.

El sector elegido es un tostadero de café de especialidad. No es casual: vende
productos con **tres tipos de IVA distintos**, y eso hace que la pantalla de
desglose por tipo impositivo, que es el diferencial de la app, se vea con tres
líneas en lugar de una.

---

## 1. Ajustes de la tienda

**Configuración → General**

- Nombre de la tienda: `Cafés Berenguer`
- Dirección: `Calle de Alcalá 45`, `28014 Madrid`, España
- Moneda: **EUR**
- Zona horaria: Madrid
- Unidad de peso: kg

La dirección de la entidad comercial pide un representante con nombre, fecha de
nacimiento y domicilio. Usa los datos reales de quien vaya a ser el titular del
negocio: no hay que inventar a nadie.

**Configuración → Impuestos y aranceles → España**

- Marca que **todos los precios incluyen impuestos**. Es lo normal en venta a
  particulares en España, y sin esto los precios se ven raros.
- Tipo general: **21%**

---

## 2. Importar productos

**Productos → Importar** y sube `productos.csv`.

Nueve productos: cuatro cafés, cuatro artículos de equipo y un libro. Precios
realistas y con decimales distintos, no todo terminado en 9,99.

---

## 3. Colecciones y tipos de IVA

Aquí está el truco que hace lucir las capturas. Shopify aplica el 21% a todo
salvo que crees excepciones por colección.

**Productos → Colecciones**, crea tres colecciones automáticas:

| Colección | Condición | IVA |
|---|---|---|
| Café | Tipo de producto es igual a `Café` | 10% |
| Equipo | Tipo de producto es igual a `Equipo` | 21% |
| Libros | Tipo de producto es igual a `Libro` | 4% |

Luego en **Configuración → Impuestos y aranceles → España → Excepciones y
exenciones**, añade una excepción para la colección `Café` al **10%** y otra para
`Libros` al **4%**. `Equipo` se queda con el general y no necesita excepción.

Con esto, un pedido que mezcle café y un molinillo genera una factura con dos
bloques de IVA. Con libro incluido, tres.

---

## 4. Importar clientes

**Clientes → Importar** y sube `clientes.csv`.

Seis clientes: cuatro particulares y dos empresas, repartidos por Valencia,
Sevilla, Barcelona, Santiago, Zaragoza y Madrid. Con acentos y eñes a propósito,
para que las capturas demuestren que el PDF los representa bien.

**Los NIF y CIF están en el campo de notas de cada cliente y son válidos de
verdad**: tienen el carácter de control correcto, así que la app los aceptará.
Un NIF inventado sería rechazado por tu propia validación.

| Cliente | Identificador |
|---|---|
| Marta Iglesias Ferrer | 46825913Y |
| Javier Ortega Ruiz | 33456789T |
| Núria Casals Puig | 52147896L |
| Ignacio Bermúdez León | 71209384G |
| Restaurante La Cepa SL | B76543214 |
| Cafetería El Molino SL | B08123457 |

---

## 5. Crear los pedidos

Los pedidos no se pueden importar por CSV. Hay que crearlos a mano en
**Pedidos → Crear pedido**, añadir el cliente y los artículos, y **Marcar como
pagado**.

Son seis. Están diseñados para que cada uno enseñe algo distinto:

| # | Cliente | Artículos | Qué demuestra |
|---|---|---|---|
| 1 | Núria Casals Puig | 2× Etiopía Yirgacheffe, 1× Filtros V60 | Dos tipos de IVA, 10% y 21% |
| 2 | Restaurante La Cepa SL | 3× Brasil Cerrado 1 kg | Factura a empresa con CIF, importe alto |
| 3 | Javier Ortega Ruiz | 1× Molinillo manual | Un solo tipo al 21% |
| 4 | Marta Iglesias Ferrer | 1× Colombia Huila, 1× El arte del café, 1× Taza | **Los tres tipos: 10%, 4% y 21%** |
| 5 | Ignacio Bermúdez León | 1× Descafeinado natural | Pedido pequeño |
| 6 | Cafetería El Molino SL | 2× Brasil Cerrado 1 kg, 1× Prensa francesa | Segunda empresa |

El pedido 4 es el que va en la captura del PDF: es el único con las tres líneas
de desglose.

**Reparte las fechas.** Shopify no deja fechar un pedido en el pasado desde el
panel, así que se crearán todos hoy. No es grave, pero si quieres que el libro
trimestral se vea poblado, créalos a lo largo de varios días.

---

## 6. Meter los NIF y emitir

En la app, **Pedidos y facturas**, introduce el NIF de cada cliente según la
tabla de arriba y pulsa **Emitir factura** en los seis.

---

## 7. La devolución

En Shopify, abre el **pedido 1** y reembolsa **1 unidad de Etiopía Yirgacheffe**.
Acuérdate de poner la cantidad, no el importe: si escribes solo dinero, el
reembolso no lleva líneas y la app no puede saber el tipo de IVA.

A los pocos segundos aparecerá la rectificativa `R-2026-0001` bajo la factura del
pedido 1. Esa fila, con la factura y su rectificativa debajo, es la mejor captura
que vas a poder hacer.

---

## 8. Comprobar antes de las capturas

- El libro del trimestre muestra tres bloques de IVA: 21%, 10% y 4%.
- Ninguna pantalla dice «Tienda ejemplo», «Pedro García» ni `12345678Z`.
- Los acentos se ven bien en los PDF: «Núria», «Bermúdez», «València».
- Incidencias está vacío o tiene un aviso que se entienda.

Ese último punto tiene truco: **un aviso bien redactado en Incidencias es una
buena captura**, porque enseña que la app protege al comerciante. Si quieres uno,
crea un pedido de más de 400 € sin NIF y deja que salte solo.
