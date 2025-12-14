import os

import pytest

from app import app as flask_app
import app as app_module


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as c:
        yield c


def test_health_endpoint_returns_ok(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.is_json
    assert resp.get_json() == {"status": "healthy"}


def test_get_db_connection_uses_env_vars(monkeypatch):
    os.environ["DB_HOST"] = "db-host"
    os.environ["DB_USER"] = "db-user"
    os.environ["DB_PASSWORD"] = "db-pass"
    os.environ["DB_NAME"] = "db-name"

    called = {}

    def fake_connect(**kwargs):
        called.update(kwargs)
        return object()

    monkeypatch.setattr(app_module.mysql.connector, "connect", fake_connect)

    _ = app_module.get_db_connection()

    assert called == {
        "host": "db-host",
        "user": "db-user",
        "password": "db-pass",
        "database": "db-name",
    }

