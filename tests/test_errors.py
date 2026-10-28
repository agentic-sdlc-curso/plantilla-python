"""Checks the shared error format with a throwaway route added only for the test."""

from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.errors import AppError
from app.main import create_app


class _Payload(BaseModel):
    name: str


def _client_with_test_routes() -> TestClient:
    app = create_app()

    @app.post("/_test/echo")
    def echo(payload: _Payload) -> dict[str, str]:
        return {"name": payload.name}

    @app.get("/_test/conflict")
    def conflict() -> None:
        raise AppError(409, "Conflict for testing")

    return TestClient(app)


def test_malformed_json_returns_400_json_error() -> None:
    res = _client_with_test_routes().post(
        "/_test/echo", content="{ not json", headers={"Content-Type": "application/json"}
    )
    assert res.status_code == 400
    assert res.json()["error"].strip() != ""


def test_validation_error_returns_400_not_422() -> None:
    res = _client_with_test_routes().post("/_test/echo", json={"name": 123})
    assert res.status_code == 400
    assert res.json()["error"].strip() != ""


def test_app_error_uses_its_status_code() -> None:
    res = _client_with_test_routes().get("/_test/conflict")
    assert res.status_code == 409
    assert res.json() == {"error": "Conflict for testing"}
