from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

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

@app.post("/polish")
async def polish_email(request: Request):
    try:
        data = await request.json()
        draft = data.get("draft", "").strip()
        tone = data.get("tone", "formal").lower()

        if not draft:
            return {"polished": "Please provide an email draft to polish."}

        cleaned_draft = " ".join(draft.split())

        # Tailored templates for each tone option
        if tone == "formal":
            polished_text = (
                f"Dear Recipient,\n\n"
                f"I hope this message finds you well. I am writing regarding the following matter: {cleaned_draft}.\n\n"
                f"Please let me know if you require any further details or clarification. Thank you for your time and cooperation.\n\n"
                f"Sincerely,\n[Your Name]"
            )
        elif tone == "concise":
            polished_text = (
                f"Summary: {cleaned_draft}. "
                f"Please review and advise on next steps at your earliest convenience."
            )
        elif tone == "casual":
            polished_text = (
                f"Hi team,\n\n"
                f"Just wanted to touch base quickly about this: {cleaned_draft}.\n\n"
                f"Let me know your thoughts when you have a sec. Thanks!\n\n"
                f"Best,\n[Your Name]"
            )
        else:
            polished_text = f"Refined Draft: {cleaned_draft}"

        # Returning under the standard "polished" key that your frontend script reads
        return {"polished": polished_text}

    except Exception as e:
        return {"polished": f"Error processing request: {str(e)}"}
