from fastapi import FastAPI
from pydantic import BaseModel
from google.generativeai import configure, GenerativeModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

class DiffRequest(BaseModel):
    diff: str

@app.post("/generate-commit")
async def generate_commit(request: DiffRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY not found in environment variables."}

    configure(api_key=api_key)

    model = GenerativeModel("gemini-1.5-flash")  # Or "gemini-1.5-pro" if needed

    prompt = f"""Act as a professional Git commit message generator.
Analyze the following code changes (git diff) and generate a concise, clear, and accurate commit message.
Use the Conventional Commits format only if appropriate (fix, docs, refactor, chore, etc.). Avoid using feat unless the change introduces a meaningful, user-facing feature.
Include specific details about what was changed (e.g., what functions were modified, what logic was updated, which conditions were altered).
Avoid listing file names unless essential.
Please write it briefly. Output only the commit message.

Here are the code changes:
{request.diff}

Commit message:"""

    response = model.generate_content(prompt)

    return {"commit_message": response.text.strip()}
