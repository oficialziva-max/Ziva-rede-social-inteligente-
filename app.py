import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Prompt(BaseModel):
    prompt: str

@app.post("/ask")
def ask(data: Prompt):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": data.prompt}],
        model="llama3-8b-8192",
    )
    return {"response": chat_completion.choices[0].message.content}
