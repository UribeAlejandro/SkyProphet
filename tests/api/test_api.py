import unittest

from fastapi.testclient import TestClient

from challenge import app


class TestBatchPipeline(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_should_get_predict(self):
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "N",
                    "MES": 3,
                    "SIGLADES": "Buenos Aires",
                    "DIANOM": "Domingo",
                }
            ]
        }

        response = self.client.post("/predict", json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"predict": [0]})

    def test_missing_feature(self):
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "N",
                    "MES": 12,
                    "SIGLADES": "Buenos Aires",
                    # Missing DIANOM
                }
            ]
        }
        response = self.client.post("/predict", json=data)

        self.assertEqual(response.status_code, 422)

    def test_mes_out_of_range(self):
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "N",
                    "MES": 13,  # Should be between 1 and 12
                    "SIGLADES": "Buenos Aires",
                    "DIANOM": "Domingo",
                }
            ]
        }

        response = self.client.post("/predict", json=data)

        self.assertEqual(response.status_code, 422)

    def test_should_failed_unknown_opera(self):
        data = {
            "flights": [
                {"OPERA": "JetSmart", "TIPOVUELO": "N", "MES": 12, "SIGLADES": "Buenos Aires", "DIANOM": "Domingo"}
            ]
        }

        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 422)

    def test_should_failed_unknown_tipo_vuelo(self):
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "O",
                    "MES": 12,
                    "SIGLADES": "Buenos Aires",
                    "DIANOM": "Domingo",
                }
            ]
        }

        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 422)

    def test_should_failed_unknown_siglades(self):
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "I",
                    "MES": 12,
                    "SIGLADES": "Havana",
                    "DIANOM": "Domingo",
                }
            ]
        }
        # when("xgboost.XGBClassifier").predict(ANY).thenReturn(np.array([0]))
        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 422)

    def test_should_failed_unknown_dianom(self):
        data = {
            "flights": [
                {
                    "OPERA": "Aerolineas Argentinas",
                    "TIPOVUELO": "I",
                    "MES": 12,
                    "SIGLADES": "Buenos Aires",
                    "DIANOM": "Juernes",
                }
            ]
        }

        response = self.client.post("/predict", json=data)
        self.assertEqual(response.status_code, 422)
