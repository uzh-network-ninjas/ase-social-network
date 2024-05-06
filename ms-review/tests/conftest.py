import pytest

from app.ReviewController import app  # Ensure this points to your FastAPI app instance
from app.ReviewService import ReviewService
from app.models.ReviewCreate import ReviewCreate
from app.models.ReviewOut import ReviewOut
from app.models.ReviewUpdate import ReviewUpdate
from app.models.ReviewListOut import ReviewListOut
from app.models.ReviewListFilteredOut import ReviewListFilteredOut
from fastapi.testclient import TestClient
from mock_review_repository import MockReviewRepository

# if want to avoid use explicit version of httpx (under February 2024)
@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here

@pytest.fixture(scope="module")
def review_service():
    yield ReviewService(MockReviewRepository())

@pytest.fixture(scope="module")
def test_review_create_model():
    return ReviewCreate

@pytest.fixture(scope="module")
def test_review_update_model():
    return ReviewUpdate

@pytest.fixture(scope="module")
def test_review_out_model():
    return ReviewOut

@pytest.fixture(scope="module")
def test_review_list_out_model():
    return ReviewListOut

@pytest.fixture(scope="module")
def test_review_list_filtered_out_model():
    return ReviewListFilteredOut