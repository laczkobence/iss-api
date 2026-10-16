import os
import requests
from fastapi import FastAPI, HTTPException
from openai import AzureOpenAI

app = FastAPI(title="ISS Tracker API", description="Live ISS position with AI commentary")

ai_client = AzureOpenAI(
    api_key=os.environ.get("AZURE_AI_KEY"),
    azure_endpoint="https://ics-foundry.openai.azure.com/",
    api_version="2024-11-01-preview"
)


@app.get("/")
def index():
    return {
        "service": "ISS Tracker API",
        "version": "1.0",
        "endpoints": {
            "GET /iss": "Get live ISS position with AI commentary"
        }
    }


@app.get("/iss")
def iss():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    if response.status_code != 200:
        raise HTTPException(status_code=503, detail="ISS API unavailable")

    data = response.json()
    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"]

    ai_response = ai_client.chat.completions.create(
        model=os.environ.get("AZURE_AI_MODEL", "gpt-4.1-mini"),
        messages=[
            {"role": "system", "content": "You are a space enthusiast assistant. Given ISS coordinates, describe where it is flying over in a short, interesting way. Include the region, ocean or country, and one fun fact about the ISS."},
            {"role": "user", "content": f"The ISS is currently at latitude {lat}, longitude {lon}. Where is it?"}
        ],
        max_tokens=200
    )

    return {
        "latitude": lat,
        "longitude": lon,
        "commentary": ai_response.choices[0].message.content
    }
