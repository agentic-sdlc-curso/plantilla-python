"""The OpenAPI document must describe the errors the API really returns (400, not 422)."""

from typing import Any

from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.main import create_app


class _Payload(BaseModel):
    name: str


# Any: the OpenAPI document is free-form JSON.
def _schema_with_test_route() -> dict[str, Any]:
    app = create_app()

    @app.post("/_test/echo")
    def echo(payload: _Payload, verbose: bool = False) -> dict[str, str]:
        return {"name": payload.name}

    schema: dict[str, Any] = TestClient(app).get("/openapi.json").json()
    return schema


def test_no_operation_documents_422() -> None:
    schema = _schema_with_test_route()
    for path_item in schema["paths"].values():
        for operation in path_item.values():
            assert "422" not in operation["responses"]


def test_operations_with_input_document_400_with_error_body() -> None:
    schema = _schema_with_test_route()
    responses = schema["paths"]["/_test/echo"]["post"]["responses"]
    assert responses["400"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/ErrorResponse"
    }
    error_schema = schema["components"]["schemas"]["ErrorResponse"]
    assert error_schema["required"] == ["error"]
    assert error_schema["properties"]["error"]["type"] == "string"


def test_operations_without_input_do_not_document_400() -> None:
    schema = _schema_with_test_route()
    assert "400" not in schema["paths"]["/health"]["get"]["responses"]


def test_default_validation_schemas_are_removed() -> None:
    schemas = _schema_with_test_route()["components"]["schemas"]
    assert "HTTPValidationError" not in schemas
    assert "ValidationError" not in schemas
