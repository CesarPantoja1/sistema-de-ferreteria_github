# Overview: Catálogo de Productos y Configuración de Rubro

## 1. Problema y Objetivo
La ferretería gestiona su inventario con hojas de cálculo dispersas y criterios heterogéneos, lo que impide tener una definición única y confiable de qué es cada producto, cómo se mide, a qué categoría pertenece y a qué precio se compra y se vende. Sin una fuente única de verdad, los desfases entre stock físico y registrado se originan desde la base: productos duplicados, unidades de medida inconsistentes (pieza, metro, kilo, caja), categorías improvisadas y precios desactualizados.

Este módulo resuelve ese problema estableciendo el **núcleo del dominio**: la definición canónica de productos y la configuración del rubro (categorías y unidades de medida). Su objetivo principal es proveer a todos los demás módulos una entidad de producto consistente, con atributos comerciales (código, nombre, categoría, unidad de medida, precio de compra, precio de venta) y de inventario (umbral de stock mínimo), de modo que cualquier movimiento, alerta, búsqueda o reporte opere sobre una base confiable y homogénea.

## 2. Usuarios Involucrados
- **Propietario de la ferretería**: Registra, edita y desactiva productos; configura las categorías propias del rubro y las unidades de medida; y define precios y umbrales de stock mínimo. Obtiene como beneficio una base de datos de productos ordenada, actualizada y alineada con la realidad comercial del negocio.
- **Personal de mostrador / vendedor**: Consulta el detalle de un producto para verificar su unidad de medida, precio de venta y disponibilidad antes de ofrecerlo al cliente. Obtiene como beneficio información precisa y consistente para atender sin ambigüedades.

## 3. Alcance (Scope)
### Dentro del Alcance (In)
- Registro de productos con atributos comerciales y de inventario: código, nombre, categoría, unidad de medida, precio de compra, precio de venta y umbral de stock mínimo.
- Edición de los atributos comerciales y de inventario de productos existentes.
- Desactivación lógica de productos discontinuados, preservando su identidad para el historial de movimientos.
- Configuración de categorías propias del rubro (ej. plomería, electricidad, pintura, herramientas).
- Configuración de unidades de medida del rubro (pieza, metro, kilo, caja).
- Consulta del detalle de un producto por parte del personal de mostrador.
- Validación de unicidad y consistencia de los atributos del producto (código, nombre, precios, umbral mínimo).

### Fuera del Alcance (Out)
- Registro de entradas, salidas y ajustes de stock (pertenece a *Control de Existencias y Movimientos*).
- Cálculo, evaluación y notificación de alertas de stock mínimo (pertenece a *Alertas de Stock Mínimo y Reposición*).
- Búsqueda y filtrado de productos por nombre, código o categoría con visualización de stock vigente (pertenece a *Búsqueda y Consulta Rápida*).
- Valorización de inventario, análisis de rotación y reportes por rango de fechas (pertenece a *Reportes de Inventario y Rotación*).
- Facturación electrónica, emisión de comprobantes fiscales y gestión de clientes.
- Integración con pasarelas de pago o terminales punto de venta.
- Compras multi-sucursal o multi-almacén.
- Actualización automática de precios desde fuentes externas o proveedores.
- Aplicación móvil nativa (solo versión web responsive).

## 4. Dependencias y Restricciones
- **Upstream**: Ninguna. Este es un módulo fundacional. Define las entidades (producto, categoría, unidad de medida) sobre las que operan todos los módulos posteriores del roadmap.
- **Restricciones**:
  - Los precios de compra y venta se actualizan manualmente por el propietario.
  - La interfaz debe ser usable por personal sin formación técnica previa.
  - La solución debe operar con infraestructura de bajo costo (hosting básico y base de datos ligera).
  - El negocio opera en una única ubicación física, por lo que no se contempla segmentación por sucursal o almacén.