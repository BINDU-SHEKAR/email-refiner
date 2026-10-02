from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import requests

app = FastAPI()

# Updated to the new Hugging Face router URL to fix DNS errors
API_URL = "https://router.huggingface.co/models/distilgpt2"
print("API_URL =", API_URL)

# Hardcoded your token so it works instantly without relying on a .env file
hf_token = "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"
headers = {
    "Authorization": f"Bearer {hf_token}"
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.get("/test")
async def test():
    return {
        "token_exists": hf_token is not None
    }


@app.post("/polish")
async def polish_email(request: Request):
    try:
        data = await request.json()

        draft = data.get("draft", "")
        tone = data.get("tone", "formal")

        prompt = (
            f"Rewrite the following email in a {tone} tone. "
            f"Keep it concise, professional, and limited to 4-6 sentences. "
            f"Do not add unrelated details:\n\n{draft}"
        )

        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=30
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        response.raise_for_status()

        result = response.json()

        if isinstance(result, list) and len(result) > 0:
            return {
                "polished": result[0].get("generated_text", "")
            }

        return {
            "error": result
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Hugging Face API request failed: {str(e)}"
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }
