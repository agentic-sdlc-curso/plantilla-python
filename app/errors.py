"""Application-wide errors and their HTTP translation.

Every error response of the API has the shape {"error": "<message>"}.
"""

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException


class ErrorResponse(BaseModel):
    """Body of every error response."""

    error: str


class AppError(Exception):
    """Business error with the HTTP status code it must produce."""

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def _error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"error": message})


async def _app_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppError)
    return _error_response(exc.status_code, exc.message)


async def _http_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    return _error_response(exc.status_code, str(exc.detail))


async def _validation_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    errors = exc.errors()
    if any(error.get("type") == "json_invalid" for error in errors):
        return _error_response(400, "Invalid JSON body")
    first = errors[0] if errors else {}
    location = ".".join(str(part) for part in first.get("loc", ()) if part != "body")
    message = str(first.get("msg", "Invalid request"))
    return _error_response(400, f"{location}: {message}" if location else message)


def register_error_handlers(app: FastAPI) -> None:
    """Translate every error to {"error": ...}. Validation errors become 400, not 422."""
    app.add_exception_handler(AppError, _app_error_handler)
    app.add_exception_handler(StarletteHTTPException, _http_error_handler)
    app.add_exception_handler(RequestValidationError, _validation_error_handler)


_ERROR_SCHEMA_REF = {"$ref": "#/components/schemas/ErrorResponse"}


# Any: OpenAPI documents are free-form JSON and FastAPI.openapi() is typed dict[str, Any].
def _document_validation_errors_as_400(schema: dict[str, Any]) -> None:
    """Replace the default 422 responses with the 400 {"error": ...} the API really returns."""
    replaced = False
    for path_item in schema.get("paths", {}).values():
        for operation in path_item.values():
            responses = operation.get("responses", {})
            if "422" not in responses:
                continue
            del responses["422"]
            responses.setdefault(
                "400",
                {
                    "description": "Invalid request",
                    "content": {"application/json": {"schema": _ERROR_SCHEMA_REF}},
                },
            )
            replaced = True
    components = schema.setdefault("components", {})
    schemas = components.setdefault("schemas", {})
    schemas.pop("HTTPValidationError", None)
    schemas.pop("ValidationError", None)
    if replaced:
        schemas["ErrorResponse"] = ErrorResponse.model_json_schema()
    if not schemas:
        del components["schemas"]
    if not components:
        del schema["components"]


class ServiceRequestsAPI(FastAPI):
    """FastAPI application whose OpenAPI schema documents the real error responses."""

    # Any: same signature as FastAPI.openapi().
    def openapi(self) -> dict[str, Any]:
        if self.openapi_schema is not None:
            return self.openapi_schema
        schema = super().openapi()
        _document_validation_errors_as_400(schema)
        return schema
