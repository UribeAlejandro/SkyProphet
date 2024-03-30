from challenge.pipeline.serving import get_model_from_registry, inference_pipeline
from tests.constants import data


def test_get_model_from_registry():
    model = get_model_from_registry()
    assert model is not None
    assert hasattr(model, "predict")


def test_inference_pipeline():
    preds = inference_pipeline(data)
    assert len(preds) == len(data)
    assert all(isinstance(pred, int) for pred in preds)
