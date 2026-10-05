# Sistema de ferretería

Proyecto generado por KOSMO (Spec-Driven Development).

## Verificar sin levantar servidores

**Backend:**
```bash
uv sync
python -m compileall app
python -c "from app.main import app"   # importa la app (valida cableado, sin HTTP)
ruff check .
pytest                                  # tests con TestClient/httpx (sin servidores)
```

**Frontend:**
```bash
bun install
bunx tsc --noEmit                        # typecheck
bunx eslint .
bun test                                # tests de componentes (Vitest + Testing Library)
bun run build                           # build de producción (sin dev server)
```

## Ejecutar (manual, cuando quieras)

```bash
uv run uvicorn app.main:app --reload --port 8000
bun run dev
```

## Despliegue (Render)

El repo incluye `render.yaml` (Blueprint) y `Dockerfile` escritos por KOSMO.
NO los modifiques: se re-escriben canónicamente y se validan antes de cada push.
Render los usa tal cual: API en `/health`, CORS por `BACKEND_CORS_ORIGINS`, frontend
estático en `dist/` con rewrite SPA (cualquier ruta sirve `index.html`) y
`VITE_API_URL` apunta a `https://{slug}-api.onrender.com/api`.
El nombre del Blueprint en Render es libre (solo es una etiqueta); los nombres de
los servicios y sus URLs los define este `render.yaml`.
ATENCIÓN free tier: SQLite es efímero — los datos se pierden al dormir/redeployar.
Para persistencia usa Postgres (el backend ya soporta `DATABASE_URL` postgresql://)
o un plan pago.
