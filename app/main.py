import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY")) # Só 1 variável

class Ask(BaseModel):
    prompt: str

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/ask")
async def ask_ziva(body: Ask):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": f"Você é a ZIVA, uma IA. Responda em pt-BR, curto: {body.prompt}"}],
        model="llama3-8b-8192", # Groq é grátis e rápido
    )
    return {"resposta": chat_completion.choices[0].message.content}
