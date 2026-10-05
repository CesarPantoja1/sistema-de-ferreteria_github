from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.catalogo.repositories import (
    CategoriaRepository,
    ProductoRepository,
    UnidadMedidaRepository,
)
from backend.catalogo.schemas import (
    CategoriaCreate,
    CategoriaRead,
    CategoriaUpdate,
    ProductoCreate,
    ProductoRead,
    ProductoUpdate,
    UnidadMedidaCreate,
    UnidadMedidaRead,
    UnidadMedidaUpdate,
)
from backend.catalogo.services import CatalogoService
from backend.database import get_db

router = APIRouter(prefix="/api/catalogo", tags=["catalogo"])


def get_service(db: Session = Depends(get_db)) -> CatalogoService:
    return CatalogoService(
        categoria_repository=CategoriaRepository(db),
        unidad_medida_repository=UnidadMedidaRepository(db),
        producto_repository=ProductoRepository(db),
    )


# ----------------------------------------------------------------------
# Categorías
# ----------------------------------------------------------------------
@router.get("/categorias", response_model=list[CategoriaRead])
def get_categorias(service: CatalogoService = Depends(get_service)) -> list[CategoriaRead]:
    return service.listar_categorias()


@router.post(
    "/categorias", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED
)
def post_categoria(
    data: CategoriaCreate, service: CatalogoService = Depends(get_service)
) -> CategoriaRead:
    return service.crear_categoria(data)


@router.put("/categorias/{categoria_id}", response_model=CategoriaRead)
def put_categoria(
    categoria_id: int,
    data: CategoriaUpdate,
    service: CatalogoService = Depends(get_service),
) -> CategoriaRead:
    return service.editar_categoria(categoria_id, data)


# ----------------------------------------------------------------------
# Unidades de medida
# ----------------------------------------------------------------------
@router.get("/unidades-medida", response_model=list[UnidadMedidaRead])
def get_unidades_medida(
    service: CatalogoService = Depends(get_service),
) -> list[UnidadMedidaRead]:
    return service.listar_unidades_medida()


@router.post(
    "/unidades-medida",
    response_model=UnidadMedidaRead,
    status_code=status.HTTP_201_CREATED,
)
def post_unidad_medida(
    data: UnidadMedidaCreate, service: CatalogoService = Depends(get_service)
) -> UnidadMedidaRead:
    return service.crear_unidad_medida(data)


@router.put("/unidades-medida/{unidad_id}", response_model=UnidadMedidaRead)
def put_unidad_medida(
    unidad_id: int,
    data: UnidadMedidaUpdate,
    service: CatalogoService = Depends(get_service),
) -> UnidadMedidaRead:
    return service.editar_unidad_medida(unidad_id, data)


# ----------------------------------------------------------------------
# Productos
# ----------------------------------------------------------------------
@router.get("/productos", response_model=list[ProductoRead])
def get_productos(
    solo_activos: bool = True, service: CatalogoService = Depends(get_service)
) -> list[ProductoRead]:
    return service.listar_productos(solo_activos=solo_activos)


@router.post(
    "/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED
)
def post_producto(
    data: ProductoCreate, service: CatalogoService = Depends(get_service)
) -> ProductoRead:
    return service.crear_producto(data)


@router.get("/productos/{producto_id}", response_model=ProductoRead)
def get_producto(
    producto_id: int, service: CatalogoService = Depends(get_service)
) -> ProductoRead:
    return service.obtener_producto(producto_id)


@router.put("/productos/{producto_id}", response_model=ProductoRead)
def put_producto(
    producto_id: int,
    data: ProductoUpdate,
    service: CatalogoService = Depends(get_service),
) -> ProductoRead:
    return service.editar_producto(producto_id, data)


@router.patch("/productos/{producto_id}/desactivar", response_model=ProductoRead)
def patch_producto_desactivar(
    producto_id: int, service: CatalogoService = Depends(get_service)
) -> ProductoRead:
    return service.desactivar_producto(producto_id)
