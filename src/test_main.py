"""To make some test work might be added 50 client's POST requests"""

from fastapi.testclient import TestClient
from main import CACHE, app, calc, history, welcome


client = TestClient(app)

# Add 50 requests
for value in range(50):
    if value % 2 == 0:
        response = client.post("/calc", json={"exp": value})
    else:
        response = client.post("/calc", json={"exp": chr(value + 65)})
# Welcome test
def test_welcome():
    response = client.get("/calc")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to CalcAPI"}


# Valid input data test
def test_calc_valid_input():
    response = client.post("/calc", json={"exp": "6 +  4 / 9 *2"})
    assert response.status_code == 200
    assert response.json() == {"result": 2.222}


# Invalid input data test
def test_calc_invalid_input():
    response = client.post("/calc", json={"exp": "5 + - 4"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid input data"}


# Valid history show test
def test_history_valid_show():
    response = client.get("/history")

    if CACHE == []:
        assert response.status_code == 404
        assert response.json() == {"detail": "History is empty"}
    else:
        assert response.status_code == 200
        assert response.json() is not None


# Valid history limited and status filtered test
def test_history_filter():
    response = client.get("/history/?limit=12&status=fail")

    if CACHE == []:
        assert response.status_code == 404
        assert response.json() == {"detail": "History is empty"}
    else:
        assert response.status_code == 200
        assert len(response.json()) == 12
        for value in response.json():
            assert value["status"] == "fail"
