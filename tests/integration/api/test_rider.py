from fastapi.testclient import TestClient


def test_rider_create(test_client: TestClient) -> None:
    data = {"first_name": "foo", "last_name": "bar", "email": "foobar@example.com"}
    response = test_client.post("/riders", json=data)

    assert response.status_code == 201, response.json()
    response_data = response.json()
    assert response_data["firstName"] == "foo"
    assert response_data["lastName"] == "bar"
    assert response_data["email"] == "foobar@example.com"
    assert "id" in response_data
