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
    client = genai.GenerativeModel(model_name="gemini-2.0-flash", api_key="AIzaSyCeXAp1HSnslHNXU1PIkpxLcttyUXHP87s")

    response = client.generate_content(f"""Act as a Git commit message generator.
Analyze the following code changes (git diff) and generate a concise, professional commit message.
Use the conventional commit style if applicable.
Do not include file names in the message unless necessary.

Code changes:
{request.diff}

Commit message:""")

    return {"commit_message": response.candidates[0].content.strip()}
