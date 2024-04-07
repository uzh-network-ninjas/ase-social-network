import pytest
from fastapi.testclient import TestClient
from app.ReviewController import app  # Ensure this points to your FastAPI app instance

# if want to avoid use explicit verion of httpx (under February 2024)
@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here
    
