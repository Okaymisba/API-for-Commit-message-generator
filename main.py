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
Analyze the following code changes (git diff) and generate a clear, concise, and accurate commit message.
Use the Conventional Commits format, only if appropriate (e.g., fix, docs, chore, refactor).
Do not label the change as feat unless it genuinely introduces a new user-facing feature.
Keep the message short and to the point—no unnecessary details or explanations.
Avoid including file names unless absolutely necessary.

Code changes:
{request.diff}

Commit message:"""
    )

    return {response.text.strip()}
