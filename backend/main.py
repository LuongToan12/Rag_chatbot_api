from fastapi import FastAPI
from pydantic import BaseModel
from backend.services.chatbot import ask

app = FastAPI(
    title="RAG Chatbot API",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
async def chat(req: ChatRequest):

    answer = ask(req.question)

    return {
        "question": req.question,
        "answer": answer
    }

@app.get("/")
async def root():
    return {
        "status": "running"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }