FROM python:3.12-slim

WORKDIR /app

# Dependencias del backend generado (pyproject.toml en src/backend)
COPY src/backend/pyproject.toml ./backend/pyproject.toml
COPY src/backend ./backend

RUN pip install --no-cache-dir ./backend

EXPOSE 8000
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
