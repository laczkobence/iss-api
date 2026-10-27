import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from openai import AzureOpenAI
from pydantic import BaseModel

app = FastAPI(title="ISS Tracker API", description="Live ISS position with AI chat")

ai_client = AzureOpenAI(
    api_key=os.environ.get("AZURE_AI_KEY"),
    azure_endpoint="https://ics-foundry.openai.azure.com/",
    api_version="2024-11-01-preview"
)

SYSTEM_PROMPT = "You are a space enthusiast assistant with knowledge about the ISS. You have been given the current ISS position and provided an initial commentary. Continue the conversation naturally, answering questions about the ISS, its location, space travel, or anything related."


class ChatRequest(BaseModel):
    messages: list


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

    ai_response = ai_client.chat.completions.create(
        model=os.environ.get("AZURE_AI_MODEL", "gpt-4.1-mini"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"The ISS is currently at latitude {lat}, longitude {lon}. Where is it? Give a short interesting description and one fun fact."}
        ],
        max_tokens=300
    )

    reply = ai_response.choices[0].message.content

    return {
        "latitude": lat,
        "longitude": lon,
        "commentary": reply,
        "messages": [
            {"role": "user", "content": f"ISS is at latitude {lat}, longitude {lon}"},
            {"role": "assistant", "content": reply}
        ]
    }


@app.post("/iss/chat")
def iss_chat(body: ChatRequest):
    if len(body.messages) == 0:
        raise HTTPException(status_code=422, detail="messages list cannot be empty")
    iss_response = requests.get("http://api.open-notify.org/iss-now.json")
    if iss_response.status_code != 200:
        raise HTTPException(status_code=503, detail="ISS API unavailable")

    data = iss_response.json()
    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + body.messages

    ai_response = ai_client.chat.completions.create(
        model=os.environ.get("AZURE_AI_MODEL", "gpt-4.1-mini"),
        messages=messages,
        max_tokens=300
    )

    reply = ai_response.choices[0].message.content

    return {
        "latitude": lat,
        "longitude": lon,
        "reply": reply,
        "messages": body.messages + [{"role": "assistant", "content": reply}]
    }
