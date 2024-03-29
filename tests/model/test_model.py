import json
import unittest

import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from challenge.constants import RANDOM_STATE
from challenge.pipeline.model import DelayModel


class TestModel(unittest.TestCase):
    with open("data/interim/feature_columns.json", "r") as file:
        features_dict = json.load(file)

    TARGET_COL = ["delay"]
    FEATURES_COLS = features_dict["feature_columns"]

    def setUp(self) -> None:
        super().setUp()
        self.model = DelayModel()
        self.data = pd.read_csv(filepath_or_buffer="data/raw/data.csv")

    def test_model_preprocess_for_training(self):
        features, target = self.model.preprocess(data=self.data, target_column="delay")

        assert isinstance(features, pd.DataFrame)
        assert features.shape[1] == len(self.FEATURES_COLS)
        assert set(features.columns) == set(self.FEATURES_COLS)

        assert isinstance(target, pd.DataFrame)
        assert target.shape[1] == len(self.TARGET_COL)
        assert set(target.columns) == set(self.TARGET_COL)

    def test_model_preprocess_for_serving(self):
        features, _ = self.model.preprocess(data=self.data)

        assert isinstance(features, pd.DataFrame)
        assert features.shape[1] == len(self.FEATURES_COLS)
        assert set(features.columns) == set(self.FEATURES_COLS)

    def test_model_fit(self):
        features, target = self.model.preprocess(data=self.data, target_column="delay")

        features_train, features_validation, target_train, target_validation = train_test_split(
            features, target, test_size=0.33, random_state=RANDOM_STATE
        )

        self.model.fit(features=features_train, target=target_train)

        predicted_target = self.model._model.predict(features_validation)

        report = classification_report(target_validation, predicted_target, output_dict=True)

        assert report["0"]["recall"] > 0.60
        assert report["0"]["f1-score"] > 0.70
        assert report["1"]["recall"] < 0.60
        assert report["1"]["f1-score"] < 0.30

    def test_model_predict(self):
        features, target = self.model.preprocess(data=self.data[0:100])

        self.model.fit(features=features, target=target)
        predicted_targets = self.model.predict(features=features)

        assert isinstance(predicted_targets, list)
        assert len(predicted_targets) == features.shape[0]
        assert all(isinstance(predicted_target, int) for predicted_target in predicted_targets)
