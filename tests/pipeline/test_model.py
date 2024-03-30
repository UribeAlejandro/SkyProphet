from tests.conftest import test_model  # noqa


def test_DelayModel(test_model):  # noqa
    assert test_model is not None
    assert hasattr(test_model, "predict")
    assert hasattr(test_model, "fit")
    assert hasattr(test_model, "preprocess")
    assert hasattr(test_model, "model")
