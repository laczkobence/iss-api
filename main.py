import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="ISS Tracker API", description="Live ISS position tracker")


@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/iss")
def iss():
    iss_response = requests.get("http://api.open-notify.org/iss-now.json")
    if iss_response.status_code != 200:
        raise HTTPException(status_code=503, detail="ISS API unavailable")

    data = iss_response.json()
    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"]

    return {
        "latitude": lat,
        "longitude": lon
    }
