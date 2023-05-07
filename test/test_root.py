from fastapi.testclient import TestClient
from fastapi import status
from app.main import app


client = TestClient(app)


def test_root_endpoint():
    """Respond with a status OK message"""

    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}
