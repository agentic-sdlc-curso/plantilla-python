# Arquitectura

API REST pequeña con FastAPI y datos en memoria.

## Estructura
```
app/
  main.py           # create_app(): crea la app, registra rutas y errores; `app` para uvicorn
  errors.py         # AppError y traducción de todos los errores a {"error": ...}
  requests/         # módulo de solicitudes (se completa con la historia H1)
    models.py       # modelos Pydantic de entrada y salida; tipos del dominio: ServiceRequest, RequestStatus…
    repository.py   # almacenamiento en memoria
    service.py      # reglas de negocio y validaciones
    routes.py       # APIRouter: traduce HTTP ↔ servicio
tests/              # tests con pytest + TestClient, uno por historia o módulo
docs/
  specs/            # especificaciones de las historias (H1.md, H2.md…)
  backlog/          # historias en borrador
  api.http          # peticiones de prueba manual
```

## Reglas
- Las rutas no contienen reglas de negocio: llaman al servicio.
- El servicio no conoce FastAPI: recibe y devuelve datos.
- El repositorio es el único que guarda datos. Debe poder vaciarse entre tests (`clear()`).
- Los tests usan `create_app()` con `TestClient`; nunca arrancan el servidor real.
- Los elementos comunes a toda la aplicación (errores, utilidades) van en `app/`, fuera de los módulos.
- Los errores de negocio se lanzan con `AppError(status, mensaje)`; `app/errors.py` los convierte en `{"error": ...}`.

## Modelo de datos (orientativo): `ServiceRequest`
| Campo | Tipo | Notas |
|---|---|---|
| `id` | str | Generado por la API |
| `title` | str | Obligatorio |
| `description` | str | |
| `status` | `"open" \| "in_progress" \| "closed"` | Empieza en `"open"` |
| `created_at` | str (ISO 8601) | Generado por la API |
