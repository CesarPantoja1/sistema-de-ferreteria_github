import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.catalogo import models  # noqa: F401
from backend.catalogo.repositories import (
    CategoriaRepository,
    ProductoRepository,
    UnidadMedidaRepository,
)
from backend.catalogo.services import CatalogoService
from backend.database import Base, get_db


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session: Session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def service(db_session: Session) -> CatalogoService:
    return CatalogoService(
        categoria_repository=CategoriaRepository(db_session),
        unidad_medida_repository=UnidadMedidaRepository(db_session),
        producto_repository=ProductoRepository(db_session),
    )


@pytest.fixture()
def client(db_session: Session):
    from backend.main import app

    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()
