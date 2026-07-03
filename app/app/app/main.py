from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/")
async def root():
    return {"status": "API Neon no ar"}
