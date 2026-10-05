from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


def _ahora() -> datetime:
    return datetime.now(UTC)


class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=_ahora, nullable=False)

    productos: Mapped[list["Producto"]] = relationship(back_populates="categoria")


class UnidadMedida(Base):
    __tablename__ = "unidad_medida"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=_ahora, nullable=False)

    productos: Mapped[list["Producto"]] = relationship(back_populates="unidad_medida")


class Producto(Base):
    __tablename__ = "producto"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.id"), nullable=False)
    unidad_medida_id: Mapped[int] = mapped_column(
        ForeignKey("unidad_medida.id"), nullable=False
    )
    precio_compra: Mapped[float] = mapped_column(Float, nullable=False)
    precio_venta: Mapped[float] = mapped_column(Float, nullable=False)
    umbral_stock_minimo: Mapped[float] = mapped_column(Float, nullable=False)
    activo: Mapped[bool] = mapped_column(default=True, nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=_ahora, nullable=False)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=_ahora, onupdate=_ahora, nullable=False
    )

    categoria: Mapped[Categoria] = relationship(back_populates="productos")
    unidad_medida: Mapped[UnidadMedida] = relationship(back_populates="productos")
