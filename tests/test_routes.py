import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app({"TESTING": True, "DATABASE_PATH": ":memory:"})
    with app.test_client() as client:
        yield client

def test_homepage_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Simula la tua Retribuzione Netta" in response.data

def test_homepage_post_calculation(client):
    response = client.post("/", data={"ral": "30000", "months": "13"})
    assert response.status_code == 200
    assert b"22609.54" in response.data or b"22.609,54" in response.data or b"Breakdown" in response.data

def test_homepage_post_decimal_calculation(client):
    # Verifica l'inserimento con formato italiano es. 27.456,78
    response = client.post("/", data={"ral": "27.456,78", "months": "14"})
    assert response.status_code == 200
    assert b"Breakdown" in response.data
    # 27.456,78 deve comparire formattato nel campo
    assert b"27.456,78" in response.data

def test_parameters_page(client):
    response = client.get("/parametri/")
    assert response.status_code == 200
    assert b"Gestione Parametri di Calcolo" in response.data

def test_api_calculate(client):
    response = client.post("/api/calculate", json={"ral": 30000, "months": 13})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert abs(json_data["data"]["net_annual"] - 22609.54) <= 0.05
