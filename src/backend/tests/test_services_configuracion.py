import pytest

from backend.catalogo.schemas import (
    CategoriaCreate,
    CategoriaUpdate,
    UnidadMedidaCreate,
    UnidadMedidaUpdate,
)
from backend.shared.errors import (
    RecursoDuplicadoError,
    RecursoNoEncontradoError,
    ValidacionNegocioError,
)


def test_crear_categoria_valida(service):
    categoria = service.crear_categoria(CategoriaCreate(nombre="Plomería"))
    assert categoria.id is not None
    assert categoria.nombre == "Plomería"


def test_crear_categoria_duplicada_lanza_error(service):
    service.crear_categoria(CategoriaCreate(nombre="Electricidad"))
    with pytest.raises(RecursoDuplicadoError) as exc:
        service.crear_categoria(CategoriaCreate(nombre="Electricidad"))
    assert exc.value.campo == "nombre"


def test_editar_categoria_inexistente_lanza_no_encontrado(service):
    with pytest.raises(RecursoNoEncontradoError):
        service.editar_categoria(999, CategoriaUpdate(nombre="Pintura"))


def test_editar_categoria_actualiza_nombre(service):
    categoria = service.crear_categoria(CategoriaCreate(nombre="Herramientas"))
    actualizada = service.editar_categoria(
        categoria.id, CategoriaUpdate(nombre="Herramientas manuales")
    )
    assert actualizada.id == categoria.id
    assert actualizada.nombre == "Herramientas manuales"


def test_editar_categoria_nombre_duplicado_lanza_error(service):
    service.crear_categoria(CategoriaCreate(nombre="A"))
    otra = service.crear_categoria(CategoriaCreate(nombre="B"))
    with pytest.raises(RecursoDuplicadoError):
        service.editar_categoria(otra.id, CategoriaUpdate(nombre="A"))


def test_crear_categoria_nombre_vacio_lanza_validacion(service):
    with pytest.raises(ValidacionNegocioError):
        service.crear_categoria(CategoriaCreate.model_construct(nombre="   "))


def test_listar_categorias(service):
    service.crear_categoria(CategoriaCreate(nombre="A"))
    service.crear_categoria(CategoriaCreate(nombre="B"))
    assert len(service.listar_categorias()) == 2


def test_crear_unidad_valida(service):
    unidad = service.crear_unidad_medida(UnidadMedidaCreate(nombre="Pieza"))
    assert unidad.id is not None
    assert unidad.nombre == "Pieza"


def test_crear_unidad_duplicada_lanza_error(service):
    service.crear_unidad_medida(UnidadMedidaCreate(nombre="Metro"))
    with pytest.raises(RecursoDuplicadoError):
        service.crear_unidad_medida(UnidadMedidaCreate(nombre="Metro"))


def test_editar_unidad_inexistente_lanza_no_encontrado(service):
    with pytest.raises(RecursoNoEncontradoError):
        service.editar_unidad_medida(999, UnidadMedidaUpdate(nombre="Kilo"))


def test_editar_unidad_actualiza_nombre(service):
    unidad = service.crear_unidad_medida(UnidadMedidaCreate(nombre="Caja"))
    actualizada = service.editar_unidad_medida(unidad.id, UnidadMedidaUpdate(nombre="Caja x12"))
    assert actualizada.id == unidad.id
    assert actualizada.nombre == "Caja x12"


def test_editar_unidad_nombre_duplicado_lanza_error(service):
    service.crear_unidad_medida(UnidadMedidaCreate(nombre="Unidad"))
    otra = service.crear_unidad_medida(UnidadMedidaCreate(nombre="Otra"))
    with pytest.raises(RecursoDuplicadoError):
        service.editar_unidad_medida(otra.id, UnidadMedidaUpdate(nombre="Unidad"))


def test_crear_unidad_nombre_vacio_lanza_validacion(service):
    with pytest.raises(ValidacionNegocioError):
        service.crear_unidad_medida(UnidadMedidaCreate.model_construct(nombre=""))


def test_listar_unidades(service):
    service.crear_unidad_medida(UnidadMedidaCreate(nombre="Pieza"))
    service.crear_unidad_medida(UnidadMedidaCreate(nombre="Metro"))
    assert len(service.listar_unidades_medida()) == 2
