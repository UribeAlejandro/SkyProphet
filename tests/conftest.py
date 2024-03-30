import pytest
from starlette.testclient import TestClient

from challenge.api import create_application
from challenge.pipeline.model import DelayModel


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
def test_model():
    model = DelayModel()
    yield model
