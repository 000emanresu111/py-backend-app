from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from app import schema

from main import app

client = TestClient(app)


class TestUserRegistration:
    pass



