"""Application factory and entry point (uvicorn app.main:app)."""

from fastapi import FastAPI

from app.errors import register_error_handlers


def create_app() -> FastAPI:
    app = FastAPI(title="Service Requests API")
    register_error_handlers(app)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
