# AGENTS.md

## Entorno
- Entorno virtual en `.venv`. Usa siempre el Python del entorno: `.venv\Scripts\python` (Windows) o `.venv/bin/python` (Linux y macOS).
- Crear el entorno e instalar dependencias:
  - `python -m venv .venv`
  - `.venv\Scripts\python -m pip install -r requirements-dev.txt`

## Comandos
- Estilo y errores habituales: `.venv\Scripts\python -m ruff check .`
- Formato: `.venv\Scripts\python -m ruff format --check .`
- Tipos: `.venv\Scripts\python -m mypy`
- Tests: `.venv\Scripts\python -m pytest`
- Todo junto (Windows): `.\scripts\check.ps1`
- Auditoría de dependencias: `.venv\Scripts\python -m pip_audit -r requirements.txt`
- Arrancar la API: `.venv\Scripts\python -m uvicorn app.main:app --reload` (http://localhost:8000, documentación en http://localhost:8000/docs)

## Flujo de trabajo
- Cada historia tiene una especificación en `docs/specs/H<n>.md`, creada a partir de `docs/specs/_plantilla.md`.
- **No se escribe código sin una especificación con estado «Aprobada».** Si no existe o no está aprobada, detente y avisa.
- Trabaja en una rama por historia: `h<n>-descripcion-corta` (por ejemplo, `h1-crear-solicitud`).
- Ciclos de corrección: como máximo 3 intentos para que pasen los tests. Si no lo consigues, detente y explica el bloqueo.

## Verificación antes de terminar
- Ejecuta `.\scripts\check.ps1` (ruff, formato, mypy y pytest) e indica el resultado, **incluido el número de tests ejecutados y cuántos son de la historia actual**.
- Revisa `git status`: no deben aparecer `.venv/`, `__pycache__/`, cachés ni archivos generados.

## Archivos
- Puedes modificar sin pedir confirmación `app/`, `tests/` y `docs/specs/`.
- Para cualquier otro archivo (dependencias, configuración, CI, instrucciones, agentes), pide confirmación y explica el motivo.

## Dependencias
- No escribas versiones de memoria. Para añadir una dependencia: instálala con `python -m pip install <paquete>`, consulta la versión instalada con `python -m pip show <paquete>` y añádela con `==<versión>` a `requirements.txt` (producción) o `requirements-dev.txt` (desarrollo).
- `pip-audit` no debe mostrar vulnerabilidades.
