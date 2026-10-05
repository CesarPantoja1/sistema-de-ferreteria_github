from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from backend.catalogo.models import Categoria, Producto, UnidadMedida
from backend.catalogo.schemas import (
    CategoriaCreate,
    CategoriaUpdate,
    ProductoCreate,
    ProductoUpdate,
    UnidadMedidaCreate,
    UnidadMedidaUpdate,
)


class CategoriaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(self) -> list[Categoria]:
        return list(self.db.scalars(select(Categoria).order_by(Categoria.id)))

    def obtener_por_id(self, categoria_id: int) -> Categoria | None:
        return self.db.get(Categoria, categoria_id)

    def obtener_por_nombre(self, nombre: str) -> Categoria | None:
        return self.db.scalar(select(Categoria).where(Categoria.nombre == nombre))

    def crear(self, data: CategoriaCreate) -> Categoria:
        categoria = Categoria(nombre=data.nombre)
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def actualizar(self, categoria: Categoria, data: CategoriaUpdate) -> Categoria:
        categoria.nombre = data.nombre
        self.db.commit()
        self.db.refresh(categoria)
        return categoria


class UnidadMedidaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar(self) -> list[UnidadMedida]:
        return list(self.db.scalars(select(UnidadMedida).order_by(UnidadMedida.id)))

    def obtener_por_id(self, unidad_id: int) -> UnidadMedida | None:
        return self.db.get(UnidadMedida, unidad_id)

    def obtener_por_nombre(self, nombre: str) -> UnidadMedida | None:
        return self.db.scalar(select(UnidadMedida).where(UnidadMedida.nombre == nombre))

    def crear(self, data: UnidadMedidaCreate) -> UnidadMedida:
        unidad = UnidadMedida(nombre=data.nombre)
        self.db.add(unidad)
        self.db.commit()
        self.db.refresh(unidad)
        return unidad

    def actualizar(self, unidad: UnidadMedida, data: UnidadMedidaUpdate) -> UnidadMedida:
        unidad.nombre = data.nombre
        self.db.commit()
        self.db.refresh(unidad)
        return unidad


class ProductoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _con_relaciones(self, *criterios):
        return (
            select(Producto)
            .options(
                joinedload(Producto.categoria),
                joinedload(Producto.unidad_medida),
            )
            .where(*criterios)
        )

    def listar(self, solo_activos: bool = True) -> list[Producto]:
        stmt = self._con_relaciones()
        if solo_activos:
            stmt = stmt.where(Producto.activo.is_(True))
        return list(self.db.scalars(stmt.order_by(Producto.id)))

    def obtener_por_id(self, producto_id: int) -> Producto | None:
        return self.db.scalar(self._con_relaciones(Producto.id == producto_id))

    def obtener_por_codigo(self, codigo: str) -> Producto | None:
        return self.db.scalar(self._con_relaciones(Producto.codigo == codigo))

    def obtener_por_nombre(self, nombre: str) -> Producto | None:
        return self.db.scalar(self._con_relaciones(Producto.nombre == nombre))

    def crear(self, data: ProductoCreate) -> Producto:
        producto = Producto(
            codigo=data.codigo,
            nombre=data.nombre,
            categoria_id=data.categoria_id,
            unidad_medida_id=data.unidad_medida_id,
            precio_compra=data.precio_compra,
            precio_venta=data.precio_venta,
            umbral_stock_minimo=data.umbral_stock_minimo,
            activo=True,
        )
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return self.obtener_por_id(producto.id)

    def actualizar(self, producto: Producto, data: ProductoUpdate) -> Producto:
        cambios = data.model_dump(exclude_unset=True)
        for campo, valor in cambios.items():
            if valor is not None:
                setattr(producto, campo, valor)
        self.db.commit()
        self.db.refresh(producto)
        return self.obtener_por_id(producto.id)

    def desactivar(self, producto: Producto) -> Producto:
        producto.activo = False
        self.db.commit()
        self.db.refresh(producto)
        return self.obtener_por_id(producto.id)
