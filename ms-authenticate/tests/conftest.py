import pytest
from fastapi.testclient import TestClient
from app.AuthenticateController import app  

# TODO there is still some warning, if want to avoid use explicit verion of httpx (under February 2024)
@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client 
