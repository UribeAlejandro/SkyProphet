from tests.conftest import test_app  # noqa


def test_health(test_app):  # noqa
    response = test_app.get("/health")
    assert response.status_code == 200
