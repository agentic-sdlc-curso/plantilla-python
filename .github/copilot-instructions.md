# Instrucciones del proyecto

## Qué es
API REST de gestión de solicitudes (por ejemplo, «pedir un portátil» o «pedir acceso a un sistema»). Proyecto de prácticas del curso.

## Stack
- Python 3.12 o superior, con **type hints** en todo el código.
- **FastAPI** para la API y **Pydantic** para los modelos de entrada y salida.
- **pytest** con el `TestClient` de FastAPI para los tests.
- **ruff** (estilo y errores habituales) y **mypy** en modo estricto (tipos).
- Datos en memoria: no hay base de datos.

## Estilo
- Código, nombres, comentarios y **mensajes de error de la API** en inglés. Respuestas del agente al usuario en el chat, en español.
- No uses para tipos propios nombres que coincidan con los de las librerías (por ejemplo, `Request` o `Response` de FastAPI/Starlette).
- Funciones pequeñas y con nombres descriptivos. Sin `Any` ni `# type: ignore` salvo que esté justificado en un comentario.
- Las respuestas de error de la API siempre en JSON: `{ "error": "mensaje" }`. Los errores de validación devuelven **400** (no 422). Ya está resuelto en `app/errors.py`: lanza `AppError(status, mensaje)` para errores de negocio.
- Estructura y capas: ver `docs/arquitectura.md`.

## Qué no hacer
- No añadas dependencias sin explicar antes por qué hacen falta.
- No implementes nada que no esté en la especificación aprobada de la historia.
- No modifiques los tests existentes para que pasen: si un test falla, corrige el código o explica por qué el test está mal.
