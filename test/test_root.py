from main import app
from fastapi import status
from fastapi.testclient import TestClient
import datetime
import jwt


client = TestClient(app)


def test_root_endpoint():
    payload = {
        "sub": "1234321",
        "name": "test-name",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }

    jwt_token = jwt.encode(payload, 'secret_key', algorithm='HS256')

    headers = {"Authorization": f"Bearer {jwt_token}"}

    response = client.get("/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}
