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

def test_docs_returns_200():
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200
