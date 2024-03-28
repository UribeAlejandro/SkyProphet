from locust import HttpUser, task


class StressUser(HttpUser):
    @task(5)
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
            },
        )

    @task(5)
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
            },
        )

    @task(1)
    def check_health(self):
        self.client.get("/health")
