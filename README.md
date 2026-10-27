# ISS Tracker API

![Tests](https://github.com/laczkobence/iss-api/actions/workflows/tests.yml/badge.svg)

A FastAPI REST API that tracks the International Space Station in real time and answers questions about it via AI.

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Home page |
| GET | `/iss` | Current ISS position (latitude, longitude) |
| POST | `/iss/chat` | Ask the AI a question about the ISS |
| GET | `/docs` | Swagger UI |

## Live API

https://iss-tracker-api-hueadjdwfqfzd2f0.germanywestcentral-01.azurewebsites.net

## Tech stack

- **FastAPI** — Python web framework
- **Azure App Service** — deployment
- **OpenAI** — AI chat endpoint
- **pytest** — test suite (14 test cases)
- **GitHub Actions** — CI pipeline

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Run tests

```bash
python -m pytest tests/ -v
```
