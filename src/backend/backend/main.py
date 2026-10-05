import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.catalogo.routes import router as catalogo_router
from backend.database import init_db
from backend.shared.errors import (
    RecursoDuplicadoError,
    RecursoNoEncontradoError,
    ValidacionNegocioError,
)

NOMBRE_APP = "Sistema de ferretería"


def _origenes_cors() -> list[str]:
    origenes = os.environ.get("BACKEND_CORS_ORIGINS")
    if origenes:
        return [origen.strip() for origen in origenes.split(",") if origen.strip()]
    return ["http://localhost:5173", "http://localhost:3000"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=NOMBRE_APP, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origenes_cors(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _respuesta_error(exc: Exception, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"detail": getattr(exc, "mensaje", str(exc)), "campo": getattr(exc, "campo", None)},
    )


@app.exception_handler(RecursoNoEncontradoError)
async def handler_no_encontrado(request: Request, exc: RecursoNoEncontradoError) -> JSONResponse:
    return _respuesta_error(exc, 404)


@app.exception_handler(RecursoDuplicadoError)
async def handler_duplicado(request: Request, exc: RecursoDuplicadoError) -> JSONResponse:
    return _respuesta_error(exc, 409)


@app.exception_handler(ValidacionNegocioError)
async def handler_validacion(request: Request, exc: ValidacionNegocioError) -> JSONResponse:
    return _respuesta_error(exc, 422)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(catalogo_router)
