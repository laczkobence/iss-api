# Test Strategy — ISS Tracker API

## Scope

**In scope:**
- REST API endpoints: `/`, `/iss`, `/iss/chat`, `/docs`
- HTTP response codes
- Response payload structure and data validity
- Input validation and error handling

**Out of scope:**
- Frontend / HTML rendering
- AI response content quality (non-deterministic)
- Performance and load testing
- Authentication (not implemented)

---

## Test Types

### Functional tests
Verify that each endpoint returns the correct status code and expected data under normal conditions.

| Test | Endpoint | What it checks |
|---|---|---|
| `test_root_returns_200` | GET `/` | Home page loads |
| `test_iss_returns_200` | GET `/iss` | ISS endpoint responds |
| `test_iss_contains_latitude` | GET `/iss` | Latitude field present |
| `test_iss_contains_longitude` | GET `/iss` | Longitude field present |
| `test_iss_latitude_is_valid_range` | GET `/iss` | Latitude between -90 and 90 |
| `test_iss_longitude_is_valid_range` | GET `/iss` | Longitude between -180 and 180 |
| `test_chat_returns_200` | POST `/iss/chat` | Chat endpoint responds |
| `test_chat_response_has_reply` | POST `/iss/chat` | Reply field present and non-empty |
| `test_docs_returns_200` | GET `/docs` | Swagger UI loads |

### Negative tests
Verify that invalid inputs are rejected with appropriate error codes.

| Test | Input | Expected |
|---|---|---|
| Empty body `{}` | POST `/iss/chat` | 422 |
| Wrong field name `{"text": "hello"}` | POST `/iss/chat` | 422 |
| Wrong type `{"messages": "not a list"}` | POST `/iss/chat` | 422 |

### Edge case tests
Verify system behavior at the boundaries of valid input.

| Test | Input | Expected |
|---|---|---|
| Empty messages list `[]` | POST `/iss/chat` | 422 |
| Very long message (5000 chars) | POST `/iss/chat` | 200, 422, or 429 |

---

## Tools

| Tool | Purpose |
|---|---|
| `pytest` | Test runner and assertion framework |
| `requests` | HTTP client for calling the live API |
| `GitHub Actions` | CI pipeline — runs tests on every push to main |
| `conftest.py` | Shared fixtures to avoid redundant HTTP calls |

---

## Risk Areas

### External API dependency
The `/iss` endpoint depends on `api.open-notify.org`. If that service is down, ISS tests will fail regardless of our code. This is an accepted external risk.

### AI response variability
The `/iss/chat` endpoint uses an AI model. Response content is non-deterministic — tests only validate structure (reply field present, status 200), not content quality.

### Flaky tests
Tests hitting live endpoints over the internet may occasionally fail due to network timeouts or external service issues. These are not code bugs. Strategy: re-run the pipeline before investigating.

---

## CI Pipeline

Tests run automatically on every push to `main` via GitHub Actions (`.github/workflows/tests.yml`). The pipeline runs on `ubuntu-latest` using Python 3.11.

A green badge on the repository indicates all tests are currently passing.

---

## Defects Found

| ID | Endpoint | Issue | Fix |
|---|---|---|---|
| BUG-001 | POST `/iss/chat` | Empty messages list `[]` returned 500 instead of 422 | Added input validation to return 422 explicitly |
