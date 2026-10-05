# Reglas del proyecto (generado por KOSMO)

## Stack
- Backend: FastAPI + uv (uv sync). Frontend: bun (bun install, bun run dev).
- Prefiere bun/uv sobre npm/pip salvo que el proyecto lo exija.

## DAG de módulos (specs)
- Catálogo de Productos y Configuración de Rubro: —
- Control de Existencias y Movimientos: ['7635af18-0620-44ef-9d1d-1e3c52418da7']
- Alertas de Stock Mínimo y Reposición: ['7635af18-0620-44ef-9d1d-1e3c52418da7', '2d9cdaf7-dc18-414e-9908-6740fed89f6a']
- Búsqueda y Consulta Rápida: ['7635af18-0620-44ef-9d1d-1e3c52418da7', '2d9cdaf7-dc18-414e-9908-6740fed89f6a']
- Reportes de Inventario y Rotación: ['7635af18-0620-44ef-9d1d-1e3c52418da7', '2d9cdaf7-dc18-414e-9908-6740fed89f6a']

## Alcance por generación
Cada run implementa UNA spec (ver specs/{spec_id}/design_files.md) dentro de src/,
consumiendo las interfaces de sus specs upstream. No modificar módulos ajenos.
- El árbol de design_files.md usa `src/` como raíz; sus rutas coinciden con el repo.
- Paquete Python canónico: src/backend/backend/ (se importa como `backend.main`).

## Verificación (sin levantar servidores)
La verificación del agente NO levanta servidores de larga duración:
- Backend: python -m compileall app + python -c "from app.main import app" + ruff check . + pytest
- Frontend: bunx tsc --noEmit + bunx eslint . + bun run build
- PROHIBIDO levantar servidores (uvicorn/vite dev) incluso como smoke test: valida endpoints con el TestClient de FastAPI/httpx dentro de pytest (sin puertos).

## Skills disponibles (invócalas con la herramienta 'skill')
- minimalist-ui / high-end-visual-design: elige UNA estética para la UI del proyecto y sé consistente.
- test-driven-development: RED-GREEN-REFACTOR antes de escribir funcionalidad (pytest / bun test).
- verification-before-completion: muestra evidencia real (N passed, 0 errores) antes de declarar terminado.
- systematic-debugging: úsala ante cualquier bug o test rojo.

## Despliegue (Render)
REGLAS DE DESPLIEGUE (código deployable en Render):
1. backend/database.py: si existe la variable de entorno DATABASE_URL, úsala tal cual con SQLAlchemy (sqlite:///... → driver sqlite; postgresql://... → psycopg2). Si NO existe, SQLite local en ./app.db (esto deja preparado migrar a Postgres sin tocar código).
2. backend/main.py: orígenes CORS desde la variable BACKEND_CORS_ORIGINS (CSV) si existe; si no, localhost (http://localhost:5173, http://localhost:3000).
3. backend/main.py: endpoint GET /health que devuelva {"status": "ok"} (health check de Render).
4. frontend/src/api/client.ts: usa EXACTAMENTE este snippet (VITE_API_URL en Render INCLUYE el
   prefijo /api, p.ej. https://{slug}-api.onrender.com/api):
       const API_BASE = import.meta.env.VITE_API_URL ?? '/api'
5. El paquete Python del backend DEBE importarse como `backend.main` (carpeta
   src/backend/backend/ con __init__.py y main.py) — el Dockerfile canónico ejecuta
   `uvicorn backend.main:app`. NO uses otros nombres de paquete.
6. El build del frontend debe generar dist/ con `bun run build` (coincide con staticPublishPath).
7. Toda navegación del frontend usa Link/useNavigate de react-router: PROHIBIDO <a href>
   o window.location (el static site solo sirve /).
8. SECRET_KEY (si el backend firma tokens/cifra): léela del env SECRET_KEY; sin default débil
   hardcodeado en producción.
9. El título/nombre visible de la app usa el NOMBRE DEL PROYECTO (no el dominio de la spec).
10. PROHIBIDO modificar render.yaml o Dockerfile (los escribe KOSMO; se validan antes del push).


## Convenciones (steering)

