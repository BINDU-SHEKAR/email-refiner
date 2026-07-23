from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import requests

app = FastAPI()

# Hugging Face Inference API endpoint
API_URL = "https://api-inference.huggingface.co/models/distilgpt2"

# Read Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {hf_token}"}

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root route serves index.html
@app.get("/")
async def root():
    return FileResponse("static/index.html")

# Backend endpoint
@app.post("/polish")
async def polish_email(request: Request):
    try:
        data = await request.json()
        draft = data.get("draft", "")
        tone = data.get("tone", "formal")

        prompt = (
            f"Rewrite the following email in a {tone} tone. "
            f"Keep it concise, professional, and limited to 4–6 sentences. "
            f"Do not add unrelated details:\n{draft}"
        )

        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()  # catch 4xx/5xx errors
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return {"polished": result[0]["generated_text"]}
        else:
            return {"error": result}

    except requests.exceptions.RequestException as e:
        # Network or API error
        return {"error": f"Hugging Face API request failed: {str(e)}"}
    except Exception as e:
        # Any other error
        return {"error": f"Unexpected error: {str(e)}"}
