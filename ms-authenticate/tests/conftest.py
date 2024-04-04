import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

with patch.dict('os.environ', {
    "MONGO_URL": "mock_mongo_url",
    "JWT_KONG_KEY": "mock_jwt_kong_key",
    "JWT_SECRET": "mock_jwt_secret",
    "JWT_ALGORITHM": "mock_jwt_algorithm"
}):
    from app.AuthenticateController import app

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client