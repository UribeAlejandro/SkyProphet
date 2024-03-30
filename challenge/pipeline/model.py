from typing import List, Optional, Tuple, Union

import pandas as pd

from challenge.pipeline.etl import etl_pipeline
from challenge.pipeline.serving import get_model_from_registry


class DelayModel:
    def __init__(self):
        self._model = get_model_from_registry()

    @staticmethod
    def preprocess(data: pd.DataFrame, target_column: Optional[str] = None) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        features, target = etl_pipeline(data, target_column)

        return features, target

    def fit(self, features: pd.DataFrame, target: Union[pd.DataFrame, pd.Series]) -> None:
        """Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        self._model.fit(features, target)

    def predict(self, features: pd.DataFrame) -> List[int]:
        """Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        preds = self._model.predict(features)
        preds = preds.tolist()
        return preds

    @property
    def model(self):
        return self._model
