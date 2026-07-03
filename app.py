import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg
import google.generativeai as genai

app = FastAPI(title="ZIVA API")

# 1. Pega as chaves do Render
DATABASE_URL = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Trava o start se faltar chave. Evita o "status 1"
if not DATABASE_URL or not GEMINI_API_KEY:
    raise RuntimeError("ERRO: DATABASE_URL e GEMINI_API_KEY precisam estar setadas no Render")

# 3. Liga o Gemini AI Studio
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash") # Modelo novo, ativo

# 4. Modelo de dados
class Ask(BaseModel):
    prompt: str
    user_id: int | None = None # Já pronto pra usar depois com tabela users

# 5. Rotas
@app.get("/health")
async def health():
    return {"ok": True, "db": "Neon", "ai": "Gemini-2.5-Flash"}

@app.post("/ask")
async def ask_ziva(body: Ask):
    try:
        # 5.1 Pede pra IA responder como ZIVA
        response = model.generate_content(
            f"Você é a ZIVA, IA da rede social ZIVA. Seja curta, engraçada e em pt-BR. Pergunta: {body.prompt}"
        )
        resposta_texto = response.text

        # 5.2 Salva no Neon automaticamente
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS chats (id SERIAL PRIMARY KEY, user_id INT, prompt TEXT, resposta TEXT, created_at TIMESTAMPTZ DEFAULT NOW())")
                cur.execute("INSERT INTO chats (user_id, prompt, resposta) VALUES (%s, %s, %s)", (body.user_id, body.prompt, resposta_texto))
                conn.commit()

        return {"resposta": resposta_texto}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na ZIVA: {str(e)}")
