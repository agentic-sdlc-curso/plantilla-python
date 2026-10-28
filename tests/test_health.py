from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_unknown_route_returns_404_json_error(client: TestClient) -> None:
    res = client.get("/does-not-exist")
    assert res.status_code == 404
    assert isinstance(res.json()["error"], str)
    assert res.json()["error"].strip() != ""


def test_wrong_method_returns_405_json_error(client: TestClient) -> None:
    res = client.post("/health")
    assert res.status_code == 405
    assert isinstance(res.json()["error"], str)
    assert res.json()["error"].strip() != ""
