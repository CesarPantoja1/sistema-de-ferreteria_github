# Requisitos: Catálogo de Productos y Configuración de Rubro

## Requisitos

### Requisito 1: Registro de productos
**Objetivo:** Como Propietario de la ferretería, quiero registrar productos con sus atributos comerciales y de inventario, para disponer de una definición canónica y única de cada producto sobre la que operen los demás módulos.

#### Criterios de Aceptación
1. When el Propietario registra un producto con código, nombre, categoría, unidad de medida, precio de compra, precio de venta y umbral de stock mínimo, the sistema shall crear el producto con estado activo.
2. When el Propietario registra un producto, the sistema shall asociar la categoría y la unidad de medida seleccionadas a entidades previamente configuradas en el rubro.
3. If el código del producto ya existe en el catálogo, the sistema shall rechazar el registro e informar que el código debe ser único.
4. If el nombre del producto ya existe en el catálogo, the sistema shall rechazar el registro e informar que el nombre debe ser único.
5. If el precio de compra o el precio de venta no es un valor numérico mayor o igual a cero, the sistema shall rechazar el registro e informar el atributo inválido.
6. If el umbral de stock mínimo no es un valor numérico mayor o igual a cero, the sistema shall rechazar el registro e informar el atributo inválido.
7. If la categoría o la unidad de medida indicada no existe en la configuración del rubro, the sistema shall rechazar el registro e informar el atributo inválido.
8. If falta cualquiera de los atributos obligatorios (código, nombre, categoría, unidad de medida, precio de compra, precio de venta, umbral de stock mínimo), the sistema shall rechazar el registro e informar los atributos faltantes.
9. The sistema shall preservar el código y el nombre del producto como identificadores únicos dentro del catálogo.

### Requisito 2: Edición de productos
**Objetivo:** Como Propietario de la ferretería, quiero editar los atributos comerciales y de inventario de productos existentes, para mantener el catálogo alineado con la realidad comercial del negocio.

#### Criterios de Aceptación
1. When el Propietario edita uno o más atributos comerciales o de inventario de un producto existente, the sistema shall actualizar el producto conservando su identidad.
2. If el nuevo código coincide con el código de otro producto existente, the sistema shall rechazar la edición e informar que el código debe ser único.
3. If el nuevo nombre coincide con el nombre de otro producto existente, the sistema shall rechazar la edición e informar que el nombre debe ser único.
4. If el precio de compra o el precio de venta editado no es un valor numérico mayor o igual a cero, the sistema shall rechazar la edición e informar el atributo inválido.
5. If el umbral de stock mínimo editado no es un valor numérico mayor o igual a cero, the sistema shall rechazar la edición e informar el atributo inválido.
6. If la categoría o la unidad de medida editada no existe en la configuración del rubro, the sistema shall rechazar la edición e informar el atributo inválido.
7. While un producto se encuentre desactivado, the sistema shall permitir la edición de sus atributos comerciales y de inventario.
8. The sistema shall actualizar los precios de compra y venta únicamente mediante edición manual del Propietario.

### Requisito 3: Desactivación lógica de productos
**Objetivo:** Como Propietario de la ferretería, quiero desactivar productos discontinuados, para preservar su identidad en el historial de movimientos sin ofrecerlos como productos vigentes.

#### Criterios de Aceptación
1. When el Propietario desactiva un producto existente, the sistema shall marcar el producto como desactivado conservando todos sus atributos.
2. While un producto se encuentre desactivado, the sistema shall preservar su código, nombre, categoría, unidad de medida, precios y umbral de stock mínimo.
3. While un producto se encuentre desactivado, the sistema shall excluirlo del conjunto de productos vigentes del catálogo.
4. If el producto indicado no existe, the sistema shall rechazar la desactivación e informar que el producto no fue encontrado.
5. The sistema shall impedir la eliminación física de productos, manteniendo la desactivación lógica como único mecanismo de baja.

### Requisito 4: Configuración de categorías del rubro
**Objetivo:** Como Propietario de la ferretería, quiero configurar las categorías propias del rubro, para clasificar los productos según la realidad comercial del negocio.

#### Criterios de Aceptación
1. When el Propietario registra una categoría con su nombre, the sistema shall crear la categoría en la configuración del rubro.
2. If el nombre de la categoría ya existe en la configuración del rubro, the sistema shall rechazar el registro e informar que el nombre debe ser único.
3. If el nombre de la categoría está vacío, the sistema shall rechazar el registro e informar el atributo faltante.
4. When el Propietario edita el nombre de una categoría existente, the sistema shall actualizar la categoría conservando su identidad.
5. If el nuevo nombre de la categoría coincide con el de otra categoría existente, the sistema shall rechazar la edición e informar que el nombre debe ser único.
6. The sistema shall exponer las categorías configuradas como valores seleccionables al registrar o editar productos.

### Requisito 5: Configuración de unidades de medida del rubro
**Objetivo:** Como Propietario de la ferretería, quiero configurar las unidades de medida del rubro, para expresar de forma homogénea cómo se mide cada producto.

#### Criterios de Aceptación
1. When el Propietario registra una unidad de medida con su nombre, the sistema shall crear la unidad de medida en la configuración del rubro.
2. If el nombre de la unidad de medida ya existe en la configuración del rubro, the sistema shall rechazar el registro e informar que el nombre debe ser único.
3. If el nombre de la unidad de medida está vacío, the sistema shall rechazar el registro e informar el atributo faltante.
4. When el Propietario edita el nombre de una unidad de medida existente, the sistema shall actualizar la unidad de medida conservando su identidad.
5. If el nuevo nombre de la unidad de medida coincide con el de otra unidad existente, the sistema shall rechazar la edición e informar que el nombre debe ser único.
6. The sistema shall exponer las unidades de medida configuradas como valores seleccionables al registrar o editar productos.

### Requisito 6: Consulta del detalle de un producto
**Objetivo:** Como Personal de mostrador / vendedor, quiero consultar el detalle de un producto, para verificar su unidad de medida, precio de venta y disponibilidad antes de ofrecerlo al cliente.

#### Criterios de Aceptación
1. When el Personal de mostrador consulta el detalle de un producto existente, the sistema shall mostrar su código, nombre, categoría, unidad de medida, precio de compra, precio de venta y umbral de stock mínimo.
2. If el producto consultado no existe, the sistema shall informar que el producto no fue encontrado.
3. While un producto se encuentre desactivado, the sistema shall mostrar su detalle indicando su estado desactivado.
4. The sistema shall mostrar el detalle del producto sin requerir la modificación de ninguno de sus atributos.

### Requisito 7: Validación de unicidad y consistencia del catálogo
**Objetivo:** Como Propietario de la ferretería, quiero que el sistema valide la unicidad y consistencia de los atributos del producto, para garantizar una base de datos de productos confiable y homogénea.

#### Criterios de Aceptación
1. The sistema shall garantizar que el código de cada producto sea único en el catálogo.
2. The sistema shall garantizar que el nombre de cada producto sea único en el catálogo.
3. The sistema shall garantizar que todo producto referencie una categoría existente en la configuración del rubro.
4. The sistema shall garantizar que todo producto referencie una unidad de medida existente en la configuración del rubro.
5. The sistema shall garantizar que el precio de compra, el precio de venta y el umbral de stock mínimo de todo producto sean valores numéricos mayores o iguales a cero.
6. If una operación de registro o edición viola cualquiera de las reglas de unicidad o consistencia, the sistema shall rechazar la operación sin alterar el estado del catálogo.