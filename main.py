from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

nlp = pipeline(
    "text-generation",
    model="distilgpt2"   # lighter than gpt2, works on free tier
)

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

    prompt = (
        f"Rewrite the following email in a {tone} tone. "
        f"Keep it concise, professional, and limited to 4–6 sentences. "
        f"Do not add unrelated details:\n{draft}"
    )

    response = nlp(
        prompt,
        max_length=120,          # reduced length
        do_sample=True,
        num_return_sequences=1   # only one output
    )

    return {"polished": response[0]["generated_text"]}
