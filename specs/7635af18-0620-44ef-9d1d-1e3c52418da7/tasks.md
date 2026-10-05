# Tareas de Implementación: Catálogo de Productos y Configuración de Rubro

## Fase 1: Modelos de Datos y Esquemas

### TASK-001: Inicializar estructura del proyecto backend y configuración de dependencias
- **Archivo:** `src/backend/pyproject.toml`, `src/backend/backend/__init__.py`, `src/backend/backend/shared/__init__.py`, `src/backend/backend/catalogo/__init__.py`
- **Descripción:** Crear el archivo `pyproject.toml` declarando dependencias: `fastapi`, `uvicorn[standard]`, `sqlalchemy`, `pydantic`, `pydantic-settings`, `pytest`, `httpx`. Definir metadata del paquete `backend`. Crear los archivos `__init__.py` vacíos para los paquetes `backend`, `backend.shared` y `backend.catalogo`.
- **Criterio de Aceptación:** `pip install -e src/backend` (o `poetry install`) finaliza sin errores y `python -c "import backend"` funciona desde `src/backend`.
- **Dependencias:** Ninguna

### TASK-002: Configurar conexión a base de datos y sesión SQLAlchemy
- **Archivo:** `src/backend/backend/database.py`
- **Descripción:** Implementar `engine` (SQLite por defecto vía `DATABASE_URL`), `SessionLocal` (sessionmaker), `Base` (declarative_base) y la dependencia `get_db()` como generador que abre/cierra sesión. Incluir función `init_db()` que ejecute `Base.metadata.create_all(bind=engine)`.
- **Criterio de Aceptación:** Importar `from backend.database import Base, get_db, init_db` funciona; `init_db()` crea el archivo SQLite sin errores.
- **Dependencias:** TASK-001

### TASK-003: Definir modelos ORM `Categoria`, `UnidadMedida` y `Producto`
- **Archivo:** `src/backend/backend/catalogo/models.py`
- **Descripción:** Implementar las clases SQLAlchemy según el diagrama de clases:
  - `Categoria`: `id` (PK), `nombre` (String, unique, not null), `creado_en` (DateTime, default now).
  - `UnidadMedida`: `id` (PK), `nombre` (String, unique, not null), `creado_en` (DateTime, default now).
  - `Producto`: `id` (PK), `codigo` (String, unique, not null), `nombre` (String, unique, not null), `categoria_id` (FK→categoria.id, not null), `unidad_medida_id` (FK→unidad_medida.id, not null), `precio_compra` (Float, not null), `precio_venta` (Float, not null), `umbral_stock_minimo` (Float, not null), `activo` (Boolean, default True), `creado_en`, `actualizado_en` (DateTime, onupdate now). Definir relaciones `categoria` y `unidad_medida` con `relationship()`.
- **Criterio de Aceptación:** `Base.metadata.create_all(engine)` genera las tres tablas con las columnas, FKs y constraints de unicidad especificados.
- **Dependencias:** TASK-002

### TASK-004: Definir esquemas Pydantic de Categoría y Unidad de Medida
- **Archivo:** `src/backend/backend/catalogo/schemas.py`
- **Descripción:** Implementar `CategoriaCreate` (`nombre: str`), `CategoriaUpdate` (`nombre: str`), `CategoriaRead` (`id: int`, `nombre: str`, `model_config = ConfigDict(from_attributes=True)`). Análogamente `UnidadMedidaCreate`, `UnidadMedidaUpdate`, `UnidadMedidaRead`. Aplicar validación `min_length=1` al campo `nombre`.
- **Criterio de Aceptación:** Instanciar `CategoriaCreate(nombre="")` lanza `ValidationError`; `CategoriaRead.model_validate(objeto_orm)` funciona con `from_attributes`.
- **Dependencias:** TASK-003

### TASK-005: Definir esquemas Pydantic de Producto
- **Archivo:** `src/backend/backend/catalogo/schemas.py`
- **Descripción:** Añadir al mismo archivo: `ProductoCreate` (`codigo`, `nombre`, `categoria_id`, `unidad_medida_id`, `precio_compra`, `precio_venta`, `umbral_stock_minimo`), `ProductoUpdate` (todos los campos `Optional`), `ProductoRead` (`id`, `codigo`, `nombre`, `categoria: CategoriaRead`, `unidad_medida: UnidadMedidaRead`, `precio_compra`, `precio_venta`, `umbral_stock_minimo`, `activo`). Aplicar `Field(ge=0)` a los tres campos numéricos y `min_length=1` a `codigo` y `nombre`.
- **Criterio de Aceptación:** `ProductoCreate` con `precio_compra=-1` lanza `ValidationError`; `ProductoRead` serializa correctamente objetos ORM con relaciones cargadas.
- **Dependencias:** TASK-004

### TASK-006: Definir excepciones de dominio compartidas
- **Archivo:** `src/backend/backend/shared/errors.py`
- **Descripción:** Implementar excepciones de dominio: `RecursoNoEncontradoError`, `RecursoDuplicadoError`, `ValidacionNegocioError`, cada una con atributo `mensaje` y `campo` opcional. Estas serán capturadas por handlers globales en `main.py` para traducirlas a respuestas HTTP 404/409/422.
- **Criterio de Aceptación:** Importar las tres excepciones funciona; cada una acepta `mensaje` y opcionalmente `campo` en su constructor.
- **Dependencias:** TASK-001

## Fase 2: Lógica de Negocio y Endpoints API (Backend)

### TASK-007: Implementar `CategoriaRepository`
- **Archivo:** `src/backend/backend/catalogo/repositories.py`
- **Descripción:** Implementar clase `CategoriaRepository` con métodos: `listar()`, `obtener_por_id(categoria_id)`, `obtener_por_nombre(nombre)`, `crear(data: CategoriaCreate)`, `actualizar(categoria: Categoria, data: CategoriaUpdate)`. Recibe `Session` en constructor. `crear` y `actualizar` hacen `commit` + `refresh`.
- **Criterio de Aceptación:** Prueba manual con sesión SQLite: crear categoría, recuperarla por id y por nombre, actualizar nombre y verificar persistencia.
- **Dependencias:** TASK-003, TASK-004

### TASK-008: Implementar `UnidadMedidaRepository`
- **Archivo:** `src/backend/backend/catalogo/repositories.py`
- **Descripción:** Añadir clase `UnidadMedidaRepository` con métodos: `listar()`, `obtener_por_id(unidad_id)`, `obtener_por_nombre(nombre)`, `crear(data: UnidadMedidaCreate)`, `actualizar(unidad: UnidadMedida, data: UnidadMedidaUpdate)`.
- **Criterio de Aceptación:** Prueba manual: crear unidad, recuperarla por id y nombre, actualizar nombre y verificar persistencia.
- **Dependencias:** TASK-007

### TASK-009: Implementar `ProductoRepository`
- **Archivo:** `src/backend/backend/catalogo/repositories.py`
- **Descripción:** Añadir clase `ProductoRepository` con métodos: `listar(solo_activos: bool)`, `obtener_por_id(producto_id)`, `obtener_por_codigo(codigo)`, `obtener_por_nombre(nombre)`, `crear(data: ProductoCreate)`, `actualizar(producto, data: ProductoUpdate)`, `desactivar(producto)`. Usar `joinedload` para cargar `categoria` y `unidad_medida` en las consultas de lectura.
- **Criterio de Aceptación:** Prueba manual: crear producto, listar con `solo_activos=True/False`, recuperar por código y nombre, actualizar precios, desactivar y verificar `activo=False`.
- **Dependencias:** TASK-008

### TASK-010: Implementar `CatalogoService` — operaciones de Categoría
- **Archivo:** `src/backend/backend/catalogo/services.py`
- **Descripción:** Implementar clase `CatalogoService` recibiendo los tres repositorios. Métodos `crear_categoria(data)` y `editar_categoria(categoria_id, data)`: validar nombre no vacío (Req 4.3, 5.3), unicidad de nombre (Req 4.2, 4.5), lanzar `RecursoDuplicadoError` o `RecursoNoEncontradoError` según corresponda. Método `listar_categorias()`.
- **Criterio de Aceptación:** Crear categoría duplicada lanza `RecursoDuplicadoError`; editar categoría inexistente lanza `RecursoNoEncontradoError`; nombre vacío lanza `ValidacionNegocioError`.
- **Dependencias:** TASK-007, TASK-006

### TASK-011: Implementar `CatalogoService` — operaciones de Unidad de Medida
- **Archivo:** `src/backend/backend/catalogo/services.py`
- **Descripción:** Añadir métodos `crear_unidad_medida(data)`, `editar_unidad_medida(unidad_id, data)`, `listar_unidades_medida()`. Aplicar las mismas validaciones de unicidad y no-vacío que en categorías (Req 5.2, 5.3, 5.5).
- **Criterio de Aceptación:** Crear unidad duplicada lanza `RecursoDuplicadoError`; editar unidad inexistente lanza `RecursoNoEncontradoError`.
- **Dependencias:** TASK-010

### TASK-012: Implementar `CatalogoService` — creación de Producto con validaciones
- **Archivo:** `src/backend/backend/catalogo/services.py`
- **Descripción:** Añadir método `crear_producto(data: ProductoCreate)`. Validar en orden: (a) unicidad de `codigo` (Req 1.3, 7.1), (b) unicidad de `nombre` (Req 1.4, 7.2), (c) existencia de `categoria_id` (Req 1.7, 7.3), (d) existencia de `unidad_medida_id` (Req 1.7, 7.4), (e) precios y umbral ≥ 0 (Req 1.5, 1.6, 7.5). Lanzar `RecursoDuplicadoError`, `ValidacionNegocioError` o `RecursoNoEncontradoError` según corresponda. Crear con `activo=True` (Req 1.1).
- **Criterio de Aceptación:** Cada violación de regla lanza la excepción esperada con mensaje que identifica el atributo; creación válida retorna `Producto` con `activo=True`.
- **Dependencias:** TASK-009, TASK-011

### TASK-013: Implementar `CatalogoService` — edición, desactivación y consulta de Producto
- **Archivo:** `src/backend/backend/catalogo/services.py`
- **Descripción:** Añadir métodos: `editar_producto(producto_id, data: ProductoUpdate)` — validar unicidad de código/nombre excluyendo el propio producto (Req 2.2, 2.3), existencia de categoría/unidad si se envían (Req 2.6), precios/umbral ≥ 0 (Req 2.4, 2.5), permitir edición de productos desactivados (Req 2.7); `desactivar_producto(producto_id)` — marcar `activo=False` preservando atributos (Req 3.1, 3.2), lanzar `RecursoNoEncontradoError` si no existe (Req 3.4); `obtener_producto(producto_id)` — retornar producto o lanzar `RecursoNoEncontradoError` (Req 6.2); `listar_productos(solo_activos)`.
- **Criterio de Aceptación:** Editar producto con código de otro lanza `RecursoDuplicadoError`; desactivar producto inexistente lanza `RecursoNoEncontradoError`; producto desactivado sigue siendo editable y consultable.
- **Dependencias:** TASK-012

### TASK-014: Implementar `CatalogoRouter` — endpoints de Categoría y Unidad de Medida
- **Archivo:** `src/backend/backend/catalogo/routes.py`
- **Descripción:** Crear `APIRouter(prefix="/api/catalogo", tags=["catalogo"])` con dependencia `get_db` y construcción de `CatalogoService`. Endpoints: `POST /categorias` (201), `PUT /categorias/{categoria_id}`, `GET /categorias`; `POST /unidades-medida` (201), `PUT /unidades-medida/{unidad_id}`, `GET /unidades-medida`. Cada uno delega al servicio y retorna el schema `*Read` correspondiente.
- **Criterio de Aceptación:** `GET /api/catalogo/categorias` retorna `[]` inicialmente; `POST` crea y retorna 201 con el recurso; `PUT` actualiza y retorna 200.
- **Dependencias:** TASK-011

### TASK-015: Implementar `CatalogoRouter` — endpoints de Producto
- **Archivo:** `src/backend/backend/catalogo/routes.py`
- **Descripción:** Añadir endpoints: `POST /productos` (201, Req 1), `PUT /productos/{producto_id}` (Req 2), `PATCH /productos/{producto_id}/desactivar` (Req 3), `GET /productos/{producto_id}` (Req 6), `GET /productos?solo_activos=true|false` (default `true`, Req 3.3). Retornar `ProductoRead` con relaciones anidadas.
- **Criterio de Aceptación:** `POST /productos` con datos válidos retorna 201 con `categoria` y `unidad_medida` anidadas; `GET /productos/{id}` de producto desactivado retorna 200 con `activo=false`.
- **Dependencias:** TASK-013, TASK-014

### TASK-016: Configurar aplicación FastAPI con handlers de excepciones
- **Archivo:** `src/backend/backend/main.py`
- **Descripción:** Crear instancia `FastAPI(title="Catálogo de Productos")`, registrar `CatalogoRouter`, configurar CORS para el frontend (`http://localhost:5173`), y añadir `@app.exception_handler` para mapear `RecursoNoEncontradoError`→404, `RecursoDuplicadoError`→409, `ValidacionNegocioError`→422, retornando JSON `{"detail": mensaje, "campo": campo}`. Invocar `init_db()` en startup.
- **Criterio de Aceptación:** `uvicorn backend.main:app --reload` arranca sin errores; una petición que dispare `RecursoDuplicadoError` retorna HTTP 409 con `detail` descriptivo.
- **Dependencias:** TASK-015

## Fase 3: Componentes e Interfaces de Usuario (Frontend)

### TASK-017: Inicializar proyecto frontend con Vite, TypeScript y Tailwind
- **Archivo:** `src/frontend/package.json`, `src/frontend/vite.config.ts`, `src/frontend/tsconfig.json`, `src/frontend/tailwind.config.js`, `src/frontend/postcss.config.js`, `src/frontend/index.html`, `src/frontend/src/main.tsx`, `src/frontend/src/index.css`
- **Descripción:** Configurar proyecto Vite + React + TypeScript. Declarar dependencias `react`, `react-dom`, `react-router-dom`, `axios` y devDeps `vite`, `typescript`, `tailwindcss`, `postcss`, `autoprefixer`, `@types/react`. Configurar Tailwind con directivas en `index.css`. `main.tsx` monta `<App />` en `#root`. `vite.config.ts` con proxy `/api` → `http://localhost:8000`.
- **Criterio de Aceptación:** `npm install && npm run dev` levanta la app en `http://localhost:5173` mostrando la app sin errores de consola.
- **Dependencias:** Ninguna

### TASK-018: Definir tipos TypeScript del dominio
- **Archivo:** `src/frontend/src/types/catalogo.ts`
- **Descripción:** Declarar interfaces `Categoria`, `UnidadMedida`, `Producto` (con `categoria: Categoria` y `unidad_medida: UnidadMedida` anidadas), `ProductoCreate`, `ProductoUpdate`, `CategoriaCreate`, `UnidadMedidaCreate`. Reflejar exactamente los campos de los schemas Pydantic.
- **Criterio de Aceptación:** Compilación TypeScript sin errores; los tipos son importables desde componentes.
- **Dependencias:** TASK-017

### TASK-019: Implementar cliente HTTP base y módulo de API de catálogo
- **Archivo:** `src/frontend/src/api/client.ts`, `src/frontend/src/api/catalogo.ts`
- **Descripción:** `client.ts`: instancia Axios con `baseURL: '/api'` e interceptor que extrae `error.response.data.detail` y lo relanza como `Error` con ese mensaje. `catalogo.ts`: funciones `listarProductos(soloActivos)`, `obtenerProducto(id)`, `crearProducto(data)`, `editarProducto(id, data)`, `desactivarProducto(id)`, `listarCategorias()`, `crearCategoria(data)`, `editarCategoria(id, data)`, `listarUnidadesMedida()`, `crearUnidadMedida(data)`, `editarUnidadMedida(id, data)`.
- **Criterio de Aceptación:** Llamadas desde consola del navegador retornan datos del backend; errores 409/422 propagan el mensaje del backend.
- **Dependencias:** TASK-018, TASK-016

### TASK-020: Implementar componente `Layout` y enrutamiento en `App.tsx`
- **Archivo:** `src/frontend/src/components/Layout.tsx`, `src/frontend/src/App.tsx`
- **Descripción:** `Layout.tsx`: barra de navegación con enlaces a `/productos` y `/configuracion`, contenedor principal con `Outlet`. `App.tsx`: configurar `BrowserRouter` con rutas `/productos` (`ProductosPage`), `/productos/:id` (`ProductoDetallePage`), `/configuracion` (`ConfiguracionPage`), redirección de `/` a `/productos`.
- **Criterio de Aceptación:** Navegar entre las tres rutas renderiza el layout con la barra de navegación y el contenido correspondiente.
- **Dependencias:** TASK-019

### TASK-021: Implementar componente `ConfirmDialog`
- **Archivo:** `src/frontend/src/components/ConfirmDialog.tsx`
- **Descripción:** Componente modal reutilizable con props `abierto: boolean`, `titulo: string`, `mensaje: string`, `onConfirmar: () => void`, `onCancelar: () => void`. Renderizado condicional con overlay y botones "Confirmar"/"Cancelar".
- **Criterio de Aceptación:** Al pasar `abierto=true` muestra el modal; clic en "Confirmar" invoca `onConfirmar`; clic en "Cancelar" invoca `onCancelar`.
- **Dependencias:** TASK-020

### TASK-022: Implementar componente `ProductoForm`
- **Archivo:** `src/frontend/src/components/ProductoForm.tsx`
- **Descripción:** Formulario controlado con campos: `codigo`, `nombre`, `categoria_id` (select poblado desde `listarCategorias`), `unidad_medida_id` (select desde `listarUnidadesMedida`), `precio_compra`, `precio_venta`, `umbral_stock_minimo` (inputs numéricos con `min=0`). Props: `valorInicial?: Producto`, `onSubmit: (data) => Promise<void>`, `onCancelar`. Mostrar errores de validación del backend bajo cada campo. Modo creación vs edición según `valorInicial`.
- **Criterio de Aceptación:** En modo creación envía `ProductoCreate`; en modo edición precarga valores y envía `ProductoUpdate`; errores 409/422 del backend se muestran junto al campo correspondiente.
- **Dependencias:** TASK-021, TASK-019

### TASK-023: Implementar componente `ProductoTable`
- **Archivo:** `src/frontend/src/components/ProductoTable.tsx`
- **Descripción:** Tabla con columnas: código, nombre, categoría, unidad de medida, precio venta, umbral mínimo, estado (activo/desactivado). Props: `productos: Producto[]`, `onVer(id)`, `onEditar(producto)`, `onDesactivar(producto)`. Botón "Desactivar" deshabilitado si `!producto.activo`.
- **Criterio de Aceptación:** Renderiza filas con datos anidados de categoría/unidad; los callbacks se disparan con el id/producto correcto.
- **Dependencias:** TASK-018

### TASK-024: Implementar componente `CategoriaManager`
- **Archivo:** `src/frontend/src/components/CategoriaManager.tsx`
- **Descripción:** Lista de categorías con formulario inline para crear (input + botón) y edición inline (input + guardar/cancelar). Consume `listarCategorias`, `crearCategoria`, `editarCategoria`. Muestra errores de unicidad (Req 4.2, 4.5) y de nombre vacío (Req 4.3).
- **Criterio de Aceptación:** Crear categoría la añade a la lista; crear duplicada muestra mensaje de error sin alterar la lista.
- **Dependencias:** TASK-019

### TASK-025: Implementar componente `UnidadMedidaManager`
- **Archivo:** `src/frontend/src/components/UnidadMedidaManager.tsx`
- **Descripción:** Análogo a `CategoriaManager` para unidades de medida. Consume `listarUnidadesMedida`, `crearUnidadMedida`, `editarUnidadMedida`. Muestra errores de unicidad (Req 5.2, 5.5) y nombre vacío (Req 5.3).
- **Criterio de Aceptación:** Crear unidad la añade a la lista; crear duplicada muestra mensaje de error sin alterar la lista.
- **Dependencias:** TASK-024

### TASK-026: Implementar `ProductosPage`
- **Archivo:** `src/frontend/src/pages/ProductosPage.tsx`
- **Descripción:** Página principal que carga productos vía `listarProductos(true)`, muestra `ProductoTable`, botón "Nuevo producto" que abre `ProductoForm` en modal, y toggle "Mostrar desactivados" que alterna `solo_activos`. Integra `ConfirmDialog` para desactivación. Al confirmar desactivación llama `desactivarProducto` y recarga la lista.
- **Criterio de Aceptación:** Crear producto lo añade a la tabla; desactivar lo oculta al estar en modo "solo activos"; toggle muestra/oculta desactivados.
- **Dependencias:** TASK-022, TASK-023, TASK-021

### TASK-027: Implementar `ProductoDetallePage`
- **Archivo:** `src/frontend/src/pages/ProductoDetallePage.tsx`
- **Descripción:** Página que lee `id` de la URL, llama `obtenerProducto(id)` y muestra todos los atributos: código, nombre, categoría, unidad de medida, precio de compra, precio de venta, umbral de stock mínimo y estado (Req 6.1). Si el producto está desactivado, mostrar badge "Desactivado" (Req 6.3). Si no existe, mostrar mensaje "Producto no encontrado" (Req 6.2). Vista de solo lectura (Req 6.4).
- **Criterio de Aceptación:** Navegar a `/productos/:id` muestra todos los atributos; id inexistente muestra mensaje de no encontrado; producto desactivado muestra badge.
- **Dependencias:** TASK-020, TASK-019

### TASK-028: Implementar `ConfiguracionPage`
- **Archivo:** `src/frontend/src/pages/ConfiguracionPage.tsx`
- **Descripción:** Página con dos secciones: "Categorías" (`CategoriaManager`) y "Unidades de medida" (`UnidadMedidaManager`). Layout en columnas o pestañas.
- **Criterio de Aceptación:** La página renderiza ambos managers y permite crear/editar categorías y unidades desde la misma vista.
- **Dependencias:** TASK-024, TASK-025

## Fase 4: Integración, Validaciones y Pruebas

### TASK-029: Pruebas unitarias de `CatalogoService` — Categoría y Unidad de Medida
- **Archivo:** `src/backend/tests/test_services_configuracion.py`
- **Descripción:** Configurar fixture de sesión SQLite en memoria. Tests: crear categoría válida, crear duplicada lanza `RecursoDuplicadoError`, editar inexistente lanza `RecursoNoEncontradoError`, nombre vacío lanza `ValidacionNegocioError`. Repetir para unidades de medida. Cubre Req 4 y Req 5.
- **Criterio de Aceptación:** `pytest src/backend/tests/test_services_configuracion.py` pasa con todos los tests en verde.
- **Dependencias:** TASK-011

### TASK-030: Pruebas unitarias de `CatalogoService` — Producto
- **Archivo:** `src/backend/tests/test_services_producto.py`
- **Descripción:** Tests: crear producto válido con `activo=True` (Req 1.1); código duplicado (Req 1.3); nombre duplicado (Req 1.4); precio negativo (Req 1.5); umbral negativo (Req 1.6); categoría inexistente (Req 1.7); unidad inexistente (Req 1.7); editar producto desactivado (Req 2.7); desactivar preserva atributos (Req 3.2); desactivar inexistente (Req 3.4); obtener inexistente (Req 6.2).
- **Criterio de Aceptación:** `pytest src/backend/tests/test_services_producto.py` pasa con todos los tests en verde.
- **Dependencias:** TASK-013

### TASK-031: Pruebas de integración de endpoints HTTP
- **Archivo:** `src/backend/tests/test_routes_catalogo.py`
- **Descripción:** Usar `TestClient` de FastAPI con base de datos de prueba. Tests de flujo completo: crear categoría → crear unidad → crear producto → listar → obtener detalle → editar → desactivar → verificar exclusión de listado activo. Verificar códigos HTTP: 201 en creación, 200 en lectura/edición, 404 en inexistente, 409 en duplicado, 422 en validación.
- **Criterio de Aceptación:** `pytest src/backend/tests/test_routes_catalogo.py` pasa con todos los tests en verde.
- **Dependencias:** TASK-016

### TASK-032: Verificación end-to-end manual del flujo completo
- **Archivo:** N/A (verificación manual)
- **Descripción:** Con backend (`uvicorn`) y frontend (`npm run dev`) corriendo: (1) crear categorías "Plomería", "Electricidad"; (2) crear unidades "Pieza", "Metro"; (3) crear producto con esos datos; (4) verificar que aparece en la tabla; (5) editar precio de venta; (6) consultar detalle; (7) desactivar producto y verificar que desaparece del listado activo pero aparece con toggle; (8) intentar crear producto con código duplicado y verificar mensaje de error en UI.
- **Criterio de Aceptación:** Los 8 pasos se completan sin errores de consola; los mensajes de error del backend se muestran correctamente en la UI.
- **Dependencias:** TASK-026, TASK-027, TASK-028, TASK-031

### TASK-033: Verificación de reglas de unicidad y consistencia a nivel de base de datos
- **Archivo:** `src/backend/tests/test_constraints_db.py`
- **Descripción:** Tests que verifican que los constraints de la BD rechazan inserciones directas que violen unicidad de `codigo`/`nombre` en `Producto` y `nombre` en `Categoria`/`UnidadMedida`, y que las FKs impiden insertar productos con `categoria_id`/`unidad_medida_id` inexistentes. Cubre Req 7.1–7.4.
- **Criterio de Aceptación:** `pytest src/backend/tests/test_constraints_db.py` pasa; las inserciones inválidas lanzan `IntegrityError`.
- **Dependencias:** TASK-003