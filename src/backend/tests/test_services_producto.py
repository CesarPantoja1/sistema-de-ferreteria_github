import pytest

from backend.catalogo.schemas import (
    CategoriaCreate,
    ProductoCreate,
    ProductoUpdate,
    UnidadMedidaCreate,
)
from backend.shared.errors import (
    RecursoDuplicadoError,
    RecursoNoEncontradoError,
    ValidacionNegocioError,
)


@pytest.fixture()
def base(service):
    categoria = service.crear_categoria(CategoriaCreate(nombre="Plomería"))
    unidad = service.crear_unidad_medida(UnidadMedidaCreate(nombre="Pieza"))
    return categoria, unidad


def _datos(categoria_id, unidad_id, **overrides):
    data = {
        "codigo": "P-001",
        "nombre": "Tubo PVC 1/2",
        "categoria_id": categoria_id,
        "unidad_medida_id": unidad_id,
        "precio_compra": 1.0,
        "precio_venta": 2.0,
        "umbral_stock_minimo": 5.0,
    }
    data.update(overrides)
    return ProductoCreate(**data)


def test_crear_producto_valido_activo(service, base):
    categoria, unidad = base
    producto = service.crear_producto(_datos(categoria.id, unidad.id))
    assert producto.id is not None
    assert producto.activo is True
    assert producto.categoria.nombre == "Plomería"
    assert producto.unidad_medida.nombre == "Pieza"


def test_crear_producto_codigo_duplicado(service, base):
    categoria, unidad = base
    service.crear_producto(_datos(categoria.id, unidad.id))
    with pytest.raises(RecursoDuplicadoError) as exc:
        service.crear_producto(_datos(categoria.id, unidad.id, nombre="Otro"))
    assert exc.value.campo == "codigo"


def test_crear_producto_nombre_duplicado(service, base):
    categoria, unidad = base
    service.crear_producto(_datos(categoria.id, unidad.id))
    with pytest.raises(RecursoDuplicadoError) as exc:
        service.crear_producto(_datos(categoria.id, unidad.id, codigo="P-002"))
    assert exc.value.campo == "nombre"


def test_crear_producto_precio_negativo(service, base):
    categoria, unidad = base
    data = _datos(categoria.id, unidad.id).model_copy(update={"precio_compra": -1.0})
    with pytest.raises(ValidacionNegocioError):
        service.crear_producto(data)


def test_crear_producto_umbral_negativo(service, base):
    categoria, unidad = base
    data = _datos(categoria.id, unidad.id).model_copy(update={"umbral_stock_minimo": -3.0})
    with pytest.raises(ValidacionNegocioError):
        service.crear_producto(data)


def test_crear_producto_categoria_inexistente(service, base):
    _, unidad = base
    with pytest.raises(RecursoNoEncontradoError):
        service.crear_producto(_datos(999, unidad.id))


def test_crear_producto_unidad_inexistente(service, base):
    categoria, _ = base
    with pytest.raises(RecursoNoEncontradoError):
        service.crear_producto(_datos(categoria.id, 999))


def test_editar_producto_inexistente(service):
    with pytest.raises(RecursoNoEncontradoError):
        service.editar_producto(999, ProductoUpdate(precio_venta=3.0))


def test_editar_producto_actualiza_precio(service, base):
    categoria, unidad = base
    producto = service.crear_producto(_datos(categoria.id, unidad.id))
    actualizado = service.editar_producto(producto.id, ProductoUpdate(precio_venta=9.5))
    assert actualizado.id == producto.id
    assert actualizado.precio_venta == 9.5


def test_editar_producto_codigo_de_otro(service, base):
    categoria, unidad = base
    service.crear_producto(_datos(categoria.id, unidad.id, codigo="A", nombre="A"))
    segundo = service.crear_producto(_datos(categoria.id, unidad.id, codigo="B", nombre="B"))
    with pytest.raises(RecursoDuplicadoError):
        service.editar_producto(segundo.id, ProductoUpdate(codigo="A"))


def test_producto_desactivado_es_editable(service, base):
    categoria, unidad = base
    producto = service.crear_producto(_datos(categoria.id, unidad.id))
    service.desactivar_producto(producto.id)
    editado = service.editar_producto(producto.id, ProductoUpdate(precio_compra=4.0))
    assert editado.activo is False
    assert editado.precio_compra == 4.0


def test_desactivar_preserva_atributos(service, base):
    categoria, unidad = base
    producto = service.crear_producto(_datos(categoria.id, unidad.id))
    desactivado = service.desactivar_producto(producto.id)
    assert desactivado.activo is False
    assert desactivado.codigo == "P-001"
    assert desactivado.nombre == "Tubo PVC 1/2"
    assert desactivado.umbral_stock_minimo == 5.0


def test_desactivar_inexistente(service):
    with pytest.raises(RecursoNoEncontradoError):
        service.desactivar_producto(999)


def test_obtener_inexistente(service):
    with pytest.raises(RecursoNoEncontradoError):
        service.obtener_producto(999)


def test_listar_solo_activos_excluye_desactivados(service, base):
    categoria, unidad = base
    activo = service.crear_producto(_datos(categoria.id, unidad.id, codigo="A", nombre="A"))
    inactivo = service.crear_producto(_datos(categoria.id, unidad.id, codigo="B", nombre="B"))
    service.desactivar_producto(inactivo.id)

    activos = service.listar_productos(solo_activos=True)
    todos = service.listar_productos(solo_activos=False)

    assert [p.id for p in activos] == [activo.id]
    assert len(todos) == 2
