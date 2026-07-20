from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/distilgpt2"

hf_token = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {hf_token}"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/polish")
async def polish_email(request: Request):
    data = await request.json()
    draft = data.get("draft", "")
    tone = data.get("tone", "formal")

    # Build prompt with tone + draft
    prompt = (
        f"Rewrite the following email in a {tone} tone. "
        f"Keep it concise, professional, and limited to 4–6 sentences. "
        f"Do not add unrelated details:\n{draft}"
    )

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    result = response.json()

    # Handle API response safely
    if isinstance(result, list) and "generated_text" in result[0]:
        return {"polished": result[0]["generated_text"]}
    else:
        return {"error": result}
