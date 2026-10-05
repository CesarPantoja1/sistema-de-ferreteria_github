from sqlalchemy.exc import IntegrityError

from backend.catalogo.models import Categoria, Producto, UnidadMedida
from backend.catalogo.repositories import (
    CategoriaRepository,
    ProductoRepository,
    UnidadMedidaRepository,
)
from backend.catalogo.schemas import (
    CategoriaCreate,
    CategoriaUpdate,
    ProductoCreate,
    ProductoUpdate,
    UnidadMedidaCreate,
    UnidadMedidaUpdate,
)
from backend.shared.errors import (
    RecursoDuplicadoError,
    RecursoNoEncontradoError,
    ValidacionNegocioError,
)


class CatalogoService:
    def __init__(
        self,
        categoria_repository: CategoriaRepository,
        unidad_medida_repository: UnidadMedidaRepository,
        producto_repository: ProductoRepository,
    ) -> None:
        self.categorias = categoria_repository
        self.unidades = unidad_medida_repository
        self.productos = producto_repository

    # ------------------------------------------------------------------
    # Categorías
    # ------------------------------------------------------------------
    def listar_categorias(self) -> list[Categoria]:
        return self.categorias.listar()

    def crear_categoria(self, data: CategoriaCreate) -> Categoria:
        nombre = (data.nombre or "").strip()
        if not nombre:
            raise ValidacionNegocioError("El nombre de la categoría es obligatorio", "nombre")
        if self.categorias.obtener_por_nombre(nombre):
            raise RecursoDuplicadoError("El nombre de la categoría ya existe", "nombre")
        try:
            return self.categorias.crear(CategoriaCreate(nombre=nombre))
        except IntegrityError as exc:
            self.categorias.db.rollback()
            raise RecursoDuplicadoError("El nombre de la categoría ya existe", "nombre") from exc

    def editar_categoria(self, categoria_id: int, data: CategoriaUpdate) -> Categoria:
        categoria = self.categorias.obtener_por_id(categoria_id)
        if categoria is None:
            raise RecursoNoEncontradoError("Categoría no encontrada")
        nombre = (data.nombre or "").strip()
        if not nombre:
            raise ValidacionNegocioError("El nombre de la categoría es obligatorio", "nombre")
        existente = self.categorias.obtener_por_nombre(nombre)
        if existente and existente.id != categoria_id:
            raise RecursoDuplicadoError("El nombre de la categoría ya existe", "nombre")
        try:
            return self.categorias.actualizar(categoria, CategoriaUpdate(nombre=nombre))
        except IntegrityError as exc:
            self.categorias.db.rollback()
            raise RecursoDuplicadoError("El nombre de la categoría ya existe", "nombre") from exc

    # ------------------------------------------------------------------
    # Unidades de medida
    # ------------------------------------------------------------------
    def listar_unidades_medida(self) -> list[UnidadMedida]:
        return self.unidades.listar()

    def crear_unidad_medida(self, data: UnidadMedidaCreate) -> UnidadMedida:
        nombre = (data.nombre or "").strip()
        if not nombre:
            raise ValidacionNegocioError(
                "El nombre de la unidad de medida es obligatorio", "nombre"
            )
        if self.unidades.obtener_por_nombre(nombre):
            raise RecursoDuplicadoError("El nombre de la unidad de medida ya existe", "nombre")
        try:
            return self.unidades.crear(UnidadMedidaCreate(nombre=nombre))
        except IntegrityError as exc:
            self.unidades.db.rollback()
            raise RecursoDuplicadoError(
                "El nombre de la unidad de medida ya existe", "nombre"
            ) from exc

    def editar_unidad_medida(
        self, unidad_id: int, data: UnidadMedidaUpdate
    ) -> UnidadMedida:
        unidad = self.unidades.obtener_por_id(unidad_id)
        if unidad is None:
            raise RecursoNoEncontradoError("Unidad de medida no encontrada")
        nombre = (data.nombre or "").strip()
        if not nombre:
            raise ValidacionNegocioError(
                "El nombre de la unidad de medida es obligatorio", "nombre"
            )
        existente = self.unidades.obtener_por_nombre(nombre)
        if existente and existente.id != unidad_id:
            raise RecursoDuplicadoError("El nombre de la unidad de medida ya existe", "nombre")
        try:
            return self.unidades.actualizar(unidad, UnidadMedidaUpdate(nombre=nombre))
        except IntegrityError as exc:
            self.unidades.db.rollback()
            raise RecursoDuplicadoError(
                "El nombre de la unidad de medida ya existe", "nombre"
            ) from exc

    # ------------------------------------------------------------------
    # Productos
    # ------------------------------------------------------------------
    def _validar_numericos(self, data: ProductoCreate | ProductoUpdate) -> None:
        for campo in ("precio_compra", "precio_venta", "umbral_stock_minimo"):
            valor = getattr(data, campo, None)
            if valor is not None and valor < 0:
                raise ValidacionNegocioError(
                    f"El atributo {campo} debe ser un valor numérico mayor o igual a cero",
                    campo,
                )

    def crear_producto(self, data: ProductoCreate) -> Producto:
        if self.productos.obtener_por_codigo(data.codigo):
            raise RecursoDuplicadoError("El código del producto ya existe", "codigo")
        if self.productos.obtener_por_nombre(data.nombre):
            raise RecursoDuplicadoError("El nombre del producto ya existe", "nombre")
        if self.categorias.obtener_por_id(data.categoria_id) is None:
            raise RecursoNoEncontradoError(
                "La categoría indicada no existe en la configuración del rubro", "categoria_id"
            )
        if self.unidades.obtener_por_id(data.unidad_medida_id) is None:
            raise RecursoNoEncontradoError(
                "La unidad de medida indicada no existe en la configuración del rubro",
                "unidad_medida_id",
            )
        self._validar_numericos(data)
        try:
            return self.productos.crear(data)
        except IntegrityError as exc:
            self.productos.db.rollback()
            raise RecursoDuplicadoError(
                "El código o el nombre del producto ya existe", "codigo"
            ) from exc

    def editar_producto(self, producto_id: int, data: ProductoUpdate) -> Producto:
        producto = self.productos.obtener_por_id(producto_id)
        if producto is None:
            raise RecursoNoEncontradoError("Producto no encontrado")

        if data.codigo is not None:
            existente = self.productos.obtener_por_codigo(data.codigo)
            if existente and existente.id != producto_id:
                raise RecursoDuplicadoError("El código del producto ya existe", "codigo")
        if data.nombre is not None:
            existente = self.productos.obtener_por_nombre(data.nombre)
            if existente and existente.id != producto_id:
                raise RecursoDuplicadoError("El nombre del producto ya existe", "nombre")
        if (
            data.categoria_id is not None
            and self.categorias.obtener_por_id(data.categoria_id) is None
        ):
            raise RecursoNoEncontradoError(
                "La categoría indicada no existe en la configuración del rubro", "categoria_id"
            )
        if (
            data.unidad_medida_id is not None
            and self.unidades.obtener_por_id(data.unidad_medida_id) is None
        ):
            raise RecursoNoEncontradoError(
                "La unidad de medida indicada no existe en la configuración del rubro",
                "unidad_medida_id",
            )
        self._validar_numericos(data)
        try:
            return self.productos.actualizar(producto, data)
        except IntegrityError as exc:
            self.productos.db.rollback()
            raise RecursoDuplicadoError(
                "El código o el nombre del producto ya existe", "codigo"
            ) from exc

    def desactivar_producto(self, producto_id: int) -> Producto:
        producto = self.productos.obtener_por_id(producto_id)
        if producto is None:
            raise RecursoNoEncontradoError("Producto no encontrado")
        return self.productos.desactivar(producto)

    def obtener_producto(self, producto_id: int) -> Producto:
        producto = self.productos.obtener_por_id(producto_id)
        if producto is None:
            raise RecursoNoEncontradoError("Producto no encontrado")
        return producto

    def listar_productos(self, solo_activos: bool = True) -> list[Producto]:
        return self.productos.listar(solo_activos=solo_activos)
