from fastapi import FastAPI
from fastapi.testclient import TestClient

from uber.database import Database
from uber.main import create_app
from uber.settings import AppSettings


def test_create_app(test_settings: AppSettings) -> None:
    test_app = create_app(test_settings)
    assert isinstance(test_app, FastAPI)


def test_app_lifecycle(test_settings: AppSettings) -> None:
    test_app = create_app(test_settings)
    with TestClient(test_app):
        assert hasattr(test_app.state, "database")
        assert isinstance(test_app.state.database, Database)
