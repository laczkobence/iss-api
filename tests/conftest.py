import requests
import pytest

BASE_URL = "https://iss-tracker-api-hueadjdwfqfzd2f0.germanywestcentral-01.azurewebsites.net"


@pytest.fixture(scope="session")
def iss_response():
    return requests.get(f"{BASE_URL}/iss")

@pytest.fixture(scope="session")
def iss_data(iss_response):
    return iss_response.json()

@pytest.fixture(scope="session")
def chat_response():
    payload = {"messages": [{"role": "user", "content": "Where is the ISS?"}]}
    return requests.post(f"{BASE_URL}/iss/chat", json=payload)

@pytest.fixture(scope="session")
def chat_data(chat_response):
    return chat_response.json()
