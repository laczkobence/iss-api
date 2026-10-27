import requests
import pytest

BASE_URL = "https://iss-tracker-api-hueadjdwfqfzd2f0.germanywestcentral-01.azurewebsites.net"


# ── Functional tests ──────────────────────────────────────────────────────────

def test_root_returns_200():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200

def test_iss_returns_200(iss_response):
    assert iss_response.status_code == 200

def test_iss_contains_latitude(iss_data):
    assert "latitude" in iss_data

def test_iss_contains_longitude(iss_data):
    assert "longitude" in iss_data

def test_iss_latitude_is_valid_range(iss_data):
    assert -90 <= float(iss_data["latitude"]) <= 90

def test_iss_longitude_is_valid_range(iss_data):
    assert -180 <= float(iss_data["longitude"]) <= 180

def test_chat_returns_200(chat_response):
    assert chat_response.status_code == 200

def test_chat_response_has_reply(chat_data):
    assert "reply" in chat_data
    assert len(chat_data["reply"]) > 0

def test_docs_returns_200():
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200


# ── Negative tests ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("payload, description", [
    ({},                           "empty body"),
    ({"text": "hello"},            "wrong field name"),
    ({"messages": "not a list"},   "wrong type"),
])
def test_chat_invalid_payloads_return_422(payload, description):
    response = requests.post(f"{BASE_URL}/iss/chat", json=payload)
    assert response.status_code == 422


# ── Edge cases ────────────────────────────────────────────────────────────────

def test_chat_empty_messages_list():
    payload = {"messages": []}
    response = requests.post(f"{BASE_URL}/iss/chat", json=payload)
    assert response.status_code in [200, 422]

def test_chat_very_long_message():
    long_message = "a" * 5000
    payload = {"messages": [{"role": "user", "content": long_message}]}
    response = requests.post(f"{BASE_URL}/iss/chat", json=payload)
    assert response.status_code in [200, 422, 429]
