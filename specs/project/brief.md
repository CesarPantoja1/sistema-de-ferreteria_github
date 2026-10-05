# Sistema de ferretería

## Resumen Ejecutivo
Aplicación web para la gestión de inventario de una ferretería, diseñada para el propietario y el personal de mostrador. Resuelve la falta de control en tiempo real sobre existencias, entradas y salidas de productos, evitando quiebres de stock y pérdidas por descontrol.

## Problema
La ferretería gestiona su inventario de forma manual o con hojas de cálculo dispersas, lo que provoca desfases entre el stock físico y el registrado, desconocimiento de niveles mínimos de reposición y dificultad para identificar productos de alta o baja rotación. Las soluciones genéricas de inventario no se adaptan a la operativa de una ferretería (unidades por metro, kilo, caja, pieza; ventas fraccionadas; catálogo amplio y heterogéneo), y suelen ser costosas o sobredimensionadas para un negocio único.

## Público Objetivo
- **Propietario de la ferretería**: Necesita visibilidad consolidada del inventario, valorización del stock y alertas de reposición para tomar decisiones de compra sin depender de conteos manuales.
- **Personal de mostrador / vendedor**: Requiere consultar disponibilidad de productos y registrar entradas y salidas de forma rápida durante la atención al cliente, sin interrumpir la venta.

## Propuesta de Valor
Centraliza el inventario de la ferretería en una única aplicación web accesible desde cualquier dispositivo con navegador, adaptada a la naturaleza heterogénea de los productos (unidades de medida mixtas, categorías propias del rubro) y con alertas de stock mínimo que anticipan la reposición. Frente a hojas de cálculo y ERPs genéricos, ofrece simplicidad operativa, bajo costo y ajuste directo al flujo real de una ferretería.

## Capacidades Clave
1. **Catálogo de productos**: Registro de productos con código, nombre, categoría, unidad de medida, precio de compra y precio de venta.
2. **Control de existencias**: Registro de entradas y salidas que actualiza el stock en tiempo real por producto.
3. **Alertas de stock mínimo**: Definición de umbrales por producto y notificación cuando el stock cae por debajo del mínimo.
4. **Búsqueda y consulta rápida**: Filtrado por nombre, código o categoría para localizar productos durante la venta.
5. **Reportes de inventario**: Valorización del stock, productos de mayor y menor rotación, y movimientos por rango de fechas.
6. **Gestión de categorías y unidades**: Configuración de categorías propias del rubro y unidades de medida (pieza, metro, kilo, caja).

## Casos de Uso Principales
- Cuando el vendedor atiende a un cliente, puede consultar la disponibilidad de un producto por nombre o código para confirmar si hay stock antes de cerrar la venta.
- Cuando el propietario revisa el inventario al cierre del día, puede ver los productos por debajo del stock mínimo para generar la orden de compra al proveedor.
- Cuando llega mercadería del proveedor, el personal puede registrar la entrada de productos para actualizar el stock y su valorización.

## Alcance

### Dentro del Alcance
- Registro y edición de productos con atributos comerciales y de inventario.
- Registro de entradas y salidas de stock con trazabilidad de fecha y responsable.
- Alertas y listado de productos bajo stock mínimo.
- Búsqueda y filtrado de productos por nombre, código y categoría.
- Reportes básicos de existencias, valorización y movimientos.
- Gestión de categorías y unidades de medida.

### Fuera del Alcance
- Facturación electrónica y emisión de comprobantes fiscales.
- Gestión de clientes, cuentas por cobrar y créditos.
- Integración con pasarelas de pago o terminales punto de venta.
- Compras multi-sucursal o multi-almacén.
- Aplicación móvil nativa (solo versión web responsive).

### Supuestos y Dependencias
- El negocio opera en una única ubicación física.
- El personal cuenta con acceso a un dispositivo con navegador web e internet.
- Los precios de compra y venta se actualizan manualmente por el propietario.
- La conexión a internet es estable durante la jornada operativa.

## Métricas de Éxito
- **Reducción de quiebres de stock**: disminuir en 50% los productos sin existencias al momento de la venta en 3 meses.
- **Precisión de inventario**: alcanzar una diferencia menor al 5% entre stock físico y stock registrado en 2 meses.
- **Adopción operativa**: registrar el 90% de las entradas y salidas de mercadería en el sistema en 1 mes.
- **Tiempo de consulta de producto**: reducir a menos de 10 segundos la verificación de disponibilidad durante la venta en 1 mes.

## Restricciones
- Presupuesto limitado: la solución debe operar con infraestructura de bajo costo (hosting básico y base de datos ligera).
- Alcance funcional acotado a inventario: no se contemplan módulos de facturación ni contabilidad en esta fase.
- Curva de aprendizaje mínima: la interfaz debe ser usable por personal sin formación técnica previa.
- Los datos de inventario deben respaldarse periódicamente para evitar pérdidas de información.