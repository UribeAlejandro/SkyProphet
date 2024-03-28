from tests.conftest import test_app


def test_should_get_predict(test_app):
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

    response = test_app.post("/predict", json=data)

    assert response.status_code == 200
    assert response.json() == {"predict": [0]}


def test_missing_feature(test_app):
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
    response = test_app.post("/predict", json=data)

    assert response.status_code == 422


def test_mes_out_of_range(test_app):
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

    response = test_app.post("/predict", json=data)

    assert response.status_code == 422


def test_should_failed_unknown_opera(test_app):
    data = {
        "flights": [
            {"OPERA": "JetSmart", "TIPOVUELO": "N", "MES": 12, "SIGLADES": "Buenos Aires", "DIANOM": "Domingo"}
        ]
    }

    response = test_app.post("/predict", json=data)
    assert response.status_code == 422


def test_should_failed_unknown_tipo_vuelo(test_app):
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

    response = test_app.post("/predict", json=data)
    assert response.status_code == 422


def test_should_failed_unknown_siglades(test_app):
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
    response = test_app.post("/predict", json=data)
    assert response.status_code == 422


def test_should_failed_unknown_dianom(test_app):
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

    response = test_app.post("/predict", json=data)
    assert response.status_code == 422
