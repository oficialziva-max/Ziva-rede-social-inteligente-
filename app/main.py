from fastapi import FastAPI
from pydantic import BaseModel
import os
import psycopg
import google.generativeai as genai

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

class Ask(BaseModel):
    prompt: str

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/ask")
async def ask_ziva(body: Ask):
    response = model.generate_content(f"Você é a ZIVA, uma IA. Responda em pt-BR, curto: {body.prompt}")
    
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS chats (id SERIAL PRIMARY KEY, prompt TEXT, resposta TEXT)")
            cur.execute("INSERT INTO chats (prompt, resposta) VALUES (%s, %s)", (body.prompt, response.text))
            conn.commit()

    return {"resposta": response.text}
