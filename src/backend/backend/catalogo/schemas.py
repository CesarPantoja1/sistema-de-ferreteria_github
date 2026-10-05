from pydantic import BaseModel, ConfigDict, Field


class CategoriaCreate(BaseModel):
    nombre: str = Field(min_length=1)


class CategoriaUpdate(BaseModel):
    nombre: str = Field(min_length=1)


class CategoriaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str


class UnidadMedidaCreate(BaseModel):
    nombre: str = Field(min_length=1)


class UnidadMedidaUpdate(BaseModel):
    nombre: str = Field(min_length=1)


class UnidadMedidaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str


class ProductoCreate(BaseModel):
    codigo: str = Field(min_length=1)
    nombre: str = Field(min_length=1)
    categoria_id: int
    unidad_medida_id: int
    precio_compra: float = Field(ge=0)
    precio_venta: float = Field(ge=0)
    umbral_stock_minimo: float = Field(ge=0)


class ProductoUpdate(BaseModel):
    codigo: str | None = Field(default=None, min_length=1)
    nombre: str | None = Field(default=None, min_length=1)
    categoria_id: int | None = None
    unidad_medida_id: int | None = None
    precio_compra: float | None = Field(default=None, ge=0)
    precio_venta: float | None = Field(default=None, ge=0)
    umbral_stock_minimo: float | None = Field(default=None, ge=0)


class ProductoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    categoria: CategoriaRead
    unidad_medida: UnidadMedidaRead
    precio_compra: float
    precio_venta: float
    umbral_stock_minimo: float
    activo: bool
