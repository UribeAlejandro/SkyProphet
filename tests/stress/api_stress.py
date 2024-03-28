from locust import HttpUser, task
from tests.constants import data


class StressUser(HttpUser):
    @task
    def predict_argentinas(self):
        self.client.post(
            "/predict",
            json={
                "flights": [
                    {
                        "OPERA": "Aerolineas Argentinas",
                        "TIPOVUELO": "I",
                        "MES": 12,
                        "SIGLADES": "Buenos Aires",
                        "DIANOM": "Jueves",
                    }
                ]
            }
        )

    @task
    def predict_latam(self):
        self.client.post(
            "/predict",
            json={
                "flights": [
                    {
                        "OPERA": "Grupo LATAM",
                        "TIPOVUELO": "I",
                        "MES": 12,
                        "SIGLADES": "Buenos Aires",
                        "DIANOM": "Jueves",
                    }
                ]
            }
        )
