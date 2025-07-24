from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

# Define FastAPI app
app = FastAPI()


# Define request model
class DiffRequest(BaseModel):
    diff: str


# Define API endpoint
@app.post("/generate-commit")
async def generate_commit(request: DiffRequest):
    client = genai.Client(api_key="AIzaSyCeXAp1HSnslHNXU1PIkpxLcttyUXHP87s")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"""Act as a professional Git commit message generator.
Analyze the following code changes (git diff) and generate a concise, clear, and accurate commit message.
Use the Conventional Commits format only if appropriate (fix, docs, refactor, chore, etc.). Avoid using feat unless the change introduces a meaningful, user-facing feature.
Include specific details about what was changed (e.g., what functions were modified, what logic was updated, which conditions were altered).
Avoid listing file names unless essential.
Write it briefly. Output only the commit message.

Here are the code changes:
{request.diff}

Commit message:"""
    )

    return {response.text.strip()}
