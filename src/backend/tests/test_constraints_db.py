import pytest
from sqlalchemy.exc import IntegrityError

from backend.catalogo.models import Categoria, Producto, UnidadMedida


def test_nombre_categoria_unico(db_session):
    db_session.add(Categoria(nombre="Plomería"))
    db_session.commit()
    db_session.add(Categoria(nombre="Plomería"))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_nombre_unidad_unico(db_session):
    db_session.add(UnidadMedida(nombre="Pieza"))
    db_session.commit()
    db_session.add(UnidadMedida(nombre="Pieza"))
    with pytest.raises(IntegrityError):
        db_session.commit()


def _producto(categoria_id, unidad_id, **overrides):
    data = {
        "codigo": "P-001",
        "nombre": "Tubo PVC",
        "categoria_id": categoria_id,
        "unidad_medida_id": unidad_id,
        "precio_compra": 1.0,
        "precio_venta": 2.0,
        "umbral_stock_minimo": 1.0,
    }
    data.update(overrides)
    return Producto(**data)


def test_codigo_producto_unico(db_session):
    cat = Categoria(nombre="A")
    uni = UnidadMedida(nombre="Pieza")
    db_session.add_all([cat, uni])
    db_session.commit()
    db_session.add(_producto(cat.id, uni.id))
    db_session.commit()
    db_session.add(_producto(cat.id, uni.id, nombre="Otro"))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_nombre_producto_unico(db_session):
    cat = Categoria(nombre="A")
    uni = UnidadMedida(nombre="Pieza")
    db_session.add_all([cat, uni])
    db_session.commit()
    db_session.add(_producto(cat.id, uni.id))
    db_session.commit()
    db_session.add(_producto(cat.id, uni.id, codigo="P-002"))
    with pytest.raises(IntegrityError):
        db_session.commit()
