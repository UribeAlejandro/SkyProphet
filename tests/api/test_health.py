import pytest
from starlette.testclient import TestClient

from challenge.api import create_application


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down


def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {
        "environment": "dev",
        "ping": "pong!",
        "testing": True,
    }
