from collections.abc import Iterable
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from uber.models.rider import Rider


def test_rider_create(test_client: TestClient) -> None:
    data = {"first_name": "foo", "last_name": "bar", "email": "foobar@example.com"}
    response = test_client.post("/riders", json=data)

    assert response.status_code == 201, response.json()
    response_data = response.json()
    assert response_data["firstName"] == "foo"
    assert response_data["lastName"] == "bar"
    assert response_data["email"] == "foobar@example.com"
    assert "id" in response_data


def test_get_rider_with_id(test_client: TestClient, create_rider: Rider) -> None:
    response = test_client.get(f"/riders/{create_rider.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert UUID(response_data["id"]) == create_rider.id
    assert response_data["firstName"] == create_rider.first_name
    assert response_data["lastName"] == create_rider.last_name
    assert response_data["email"] == create_rider.email


def test_get_rider_with_raises_rider_not_found(
    test_client: TestClient,
) -> None:
    response = test_client.get(f"/riders/{uuid4()}")
    response_data = response.json()
    assert response.status_code == 404
    assert response_data["error"]["code"] == "RIDER_NOT_FOUND"
    assert response_data["error"]["message"] == "Rider not found"


def test_get_all_riders_paginated(
    test_client: TestClient, create_multiple_riders: Iterable[Rider]
) -> None:
    response = test_client.get("/riders")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["items"]) == 5
    assert response_data["pageNumber"] == 1
    assert response_data["pageSize"] == 20
    assert response_data["totalItems"] == 5
