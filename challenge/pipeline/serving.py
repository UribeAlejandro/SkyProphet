from functools import lru_cache
from typing import List

import mlflow
import pandas as pd

from challenge.constants import MLFLOW_EXPERIMENT_NAME, MLFLOW_TRACKING_URI, MODEL_STAGE
from challenge.pipeline.etl import transform_categorical


@lru_cache()
def get_model_from_registry() -> mlflow.sklearn.Model:
    """Get model from MLflow registry.

    Returns
    -------
    mlflow.sklearn.Model
        Trained model from registry.
    """
    _ = mlflow.MlflowClient(MLFLOW_TRACKING_URI)
    model = mlflow.sklearn.load_model(f"models:/{MLFLOW_EXPERIMENT_NAME}@{MODEL_STAGE}")
    return model


def enforce_schema(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Enforce schema to the data.

    Parameters
    ----------
    data : pd.DataFrame
        Data.
    columns : List[str]
        Actual schema (to be enforced).

    Returns
    -------
    pd.DataFrame
        Data with enforced schema.
    """
    df_for_pred = pd.DataFrame(0, index=data.index, columns=columns)
    df_for_pred.update(data)

    return df_for_pred


def inference_pipeline(payload: dict) -> List[int]:
    """Inference pipeline.

    Parameters
    ----------
    payload : dict
        Payload with flights data.

    Returns
    -------
    List[int]
        Predicted delays.
    """
    data = pd.DataFrame(payload["flights"])
    data = transform_categorical(data)

    model = get_model_from_registry()
    columns = model.feature_names_in_

    data = enforce_schema(data=data, columns=columns)

    delay_preds = model.predict(data).tolist()

    return delay_preds
