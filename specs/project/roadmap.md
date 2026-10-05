# Roadmap: Sistema de ferretería

## 1. Visión y Estrategia de Arquitectura

El Sistema de ferretería se concibe como un **Monolito Modular** orientado al dominio del control de inventario de una ferretería de una única ubicación física. La estrategia consiste en descomponer el producto en módulos funcionales autónomos que representan rebanadas verticales del negocio (interfaz, lógica de dominio y persistencia), evitando dependencias distribuidas y manteniendo un único despliegue de bajo costo, coherente con la restricción presupuestaria del negocio.

El desacoplamiento se organiza alrededor del **catálogo de productos como núcleo del dominio**: todo movimiento, alerta o reporte gira en torno a la definición de un producto con su unidad de medida, categoría y precios. Sobre esa base se construyen, de forma incremental, los módulos de control de existencias, alertas de reposición y analítica de inventario. Cada módulo expone responsabilidades claras y se comunica con los demás a través de contratos internos bien definidos, de modo que un cambio en la lógica de movimientos no obligue a reescribir la consulta rápida ni los reportes.

La **autonomía de los módulos** se garantiza porque cada uno posee su propia lógica de negocio y sus propias reglas de validación: el módulo de catálogo no conoce cómo se calculan las alertas, y el módulo de reportes no altera el stock, solo lo lee. Esta separación permite que el personal de mostrador opere con rapidez en la consulta y el registro de movimientos, mientras el propietario obtiene visibilidad consolidada sin interferir en la operación diaria. El resultado es un sistema simple de operar, adaptable a la naturaleza heterogénea de los productos de ferretería (pieza, metro, kilo, caja) y preparado para crecer funcionalmente sin migrar a arquitecturas distribuidas.

---

## 2. Módulos (Specs)

### 1. Catálogo de Productos y Configuración de Rubro

- **Tipo de Módulo:** core_foundation
- **Propósito:** Ser la fuente única de verdad sobre los productos de la ferretería y su configuración de rubro (categorías y unidades de medida). Define los atributos comerciales y de inventario (código, nombre, categoría, unidad de medida, precio de compra, precio de venta, umbral de stock mínimo) sobre los que operan todos los demás módulos.
- **Interacciones de Usuario (Alto Nivel):**
  - El propietario registra un nuevo producto con su código, nombre, categoría, unidad de medida, precios de compra y venta, y umbral de stock mínimo.
  - El propietario edita los atributos comerciales de un producto existente (precios, categoría, unidad de medida) cuando cambian las condiciones del proveedor.
  - El propietario configura las categorías propias del rubro (ej. plomería, electricidad, pintura, herramientas) y las unidades de medida (pieza, metro, kilo, caja).
  - El personal de mostrador consulta el detalle de un producto para verificar su unidad de medida y precio de venta antes de ofrecerlo.
  - El propietario desactiva un producto discontinuado sin eliminarlo del historial de movimientos.
- **Dependencias:** Ninguna. (Módulo Fundacional)

### 2. Control de Existencias y Movimientos

- **Tipo de Módulo:** feature_slice
- **Propósito:** Registrar entradas y salidas de mercadería y mantener el stock actualizado en tiempo real por producto, con trazabilidad de fecha y responsable. Es el motor operativo que refleja la realidad física del almacén.
- **Interacciones de Usuario (Alto Nivel):**
  - El personal de mostrador registra la entrada de mercadería recibida del proveedor, indicando producto y cantidad en la unidad de medida correspondiente.
  - El personal de mostrador registra la salida de un producto al concretar una venta, descontando el stock de forma inmediata.
  - El personal de mostrador ajusta el stock de un producto tras un conteo físico, dejando constancia del motivo del ajuste.
  - El propietario consulta el historial de movimientos de un producto específico para auditar entradas, salidas y ajustes.
  - El personal de mostrador visualiza el stock actual de un producto justo después de registrar un movimiento.
- **Dependencias:**
  - **Catálogo de Productos y Configuración de Rubro**: Todo movimiento debe referenciar un producto existente con su unidad de medida y categoría; sin el catálogo no es posible identificar sobre qué se aplica la entrada o salida.

### 3. Alertas de Stock Mínimo y Reposición

- **Tipo de Módulo:** feature_slice
- **Propósito:** Evaluar continuamente el stock de cada producto contra su umbral mínimo definido y exponer un listado accionable de productos que requieren reposición, anticipando los quiebres de stock.
- **Interacciones de Usuario (Alto Nivel):**
  - El propietario visualiza el listado de productos cuyo stock actual está por debajo del mínimo configurado.
  - El propietario ajusta el umbral de stock mínimo de un producto según su rotación real.
  - El propietario marca un producto como "reposición en curso" para excluirlo temporalmente del listado de alertas mientras llega la orden de compra.
  - El personal de mostrador recibe una advertencia visual al registrar una salida que deja el producto por debajo del mínimo.
  - El propietario exporta o imprime el listado de productos bajo mínimo para gestionar la compra al proveedor.
- **Dependencias:**
  - **Catálogo de Productos y Configuración de Rubro**: Requiere los umbrales mínimos y la identidad de cada producto para evaluar la condición de alerta.
  - **Control de Existencias y Movimientos**: Necesita el stock actualizado en tiempo real para determinar cuándo un producto cruza por debajo del umbral.

### 4. Búsqueda y Consulta Rápida

- **Tipo de Módulo:** feature_slice
- **Propósito:** Permitir la localización inmediata de productos durante la atención al cliente, filtrando por nombre, código o categoría, con el objetivo de verificar disponibilidad en menos de 10 segundos.
- **Interacciones de Usuario (Alto Nivel):**
  - El personal de mostrador busca un producto por nombre o parte del nombre para confirmar su disponibilidad durante la venta.
  - El personal de mostrador busca un producto por su código exacto cuando el cliente lo proporciona.
  - El personal de mostrador filtra productos por categoría para ofrecer alternativas dentro del mismo rubro.
  - El personal de mostrador visualiza en el resultado de búsqueda el stock disponible, la unidad de medida y el precio de venta.
  - El propietario consulta rápidamente un producto para verificar su precio o existencia sin recorrer el catálogo completo.
- **Dependencias:**
  - **Catálogo de Productos y Configuración de Rubro**: La búsqueda opera sobre los atributos indexables del producto (nombre, código, categoría).
  - **Control de Existencias y Movimientos**: El resultado de búsqueda debe mostrar el stock vigente, no un valor estático.

### 5. Reportes de Inventario y Rotación

- **Tipo de Módulo:** reporting_analytics
- **Propósito:** Ofrecer al propietario visibilidad consolidada del inventario mediante valorización del stock, identificación de productos de mayor y menor rotación, y análisis de movimientos por rango de fechas, para sustentar decisiones de compra.
- **Interacciones de Usuario (Alto Nivel):**
  - El propietario consulta la valorización total del inventario a precio de compra y a precio de venta.
  - El propietario identifica los productos de mayor rotación en un período para priorizar su reposición.
  - El propietario identifica los productos de menor rotación para evaluar su continuidad o promoción.
  - El propietario analiza los movimientos de entrada y salida por rango de fechas para conciliar con las compras y ventas del período.
  - El propietario exporta un resumen de inventario para respaldo o revisión externa.
- **Dependencias:**
  - **Catálogo de Productos y Configuración de Rubro**: Requiere precios de compra y venta, categorías y unidades para valorizar y agrupar.
  - **Control de Existencias y Movimientos**: Los reportes de rotación y movimientos se calculan sobre el historial de entradas, salidas y ajustes.

---

## 3. Matriz de Dependencias y Orden de Ejecución

| Módulo | Módulos Upstream requeridos | Tipo de Acoplamiento | Razonamiento de Orden |
|---|---|---|---|
| Catálogo de Productos y Configuración de Rubro | Ninguno | Fundacional | Punto de entrada: define las entidades (producto, categoría, unidad de medida) sobre las que operan todos los demás módulos. |
| Control de Existencias y Movimientos | Catálogo de Productos y Configuración de Rubro | Fuerte | Requiere la identidad del producto y su unidad de medida para registrar entradas, salidas y ajustes con trazabilidad. |
| Alertas de Stock Mínimo y Reposición | Catálogo de Productos y Configuración de Rubro; Control de Existencias y Movimientos | Fuerte | Necesita los umbrales mínimos del catálogo y el stock actualizado en tiempo real para evaluar la condición de alerta. |
| Búsqueda y Consulta Rápida | Catálogo de Productos y Configuración de Rubro; Control de Existencias y Movimientos | Fuerte | Indexa atributos del catálogo y debe mostrar el stock vigente proveniente del control de existencias. |
| Reportes de Inventario y Rotación | Catálogo de Productos y Configuración de Rubro; Control de Existencias y Movimientos | Fuerte | Consume precios, categorías y el historial de movimientos para valorizar el stock y calcular rotación por período. |