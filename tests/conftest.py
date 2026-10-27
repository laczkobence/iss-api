import requests
import pytest

BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def iss_response():
    return requests.get(f"{BASE_URL}/iss")

@pytest.fixture(scope="session")
def iss_data(iss_response):
    return iss_response.json()
