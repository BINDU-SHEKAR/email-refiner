from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

# Use a causal LM that works with text-generation
nlp = pipeline("text-generation", model="gpt2")

app = FastAPI()

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

    # ✅ These lines must be indented inside the function
    prompt = f"Rewrite the following email in a {tone} tone. Keep it concise, professional, and limited to 4–6 sentences. Do not add unrelated details:\n{draft}"

    response = nlp(prompt, max_length=200, do_sample=True)

    return {"polished": response[0]["generated_text"]}
