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
        model="gemini-2.0-flash", contents=f"""Act as a Git commit message generator.
    Analyze the following code changes (git diff) and generate a concise, professional commit message.
    Use the conventional commit style if applicable.
    Do not include file names in the message unless necessary.

    Code changes:
    {request.diff}


    Commit message:"""
    )

    return {response.text.strip()}
