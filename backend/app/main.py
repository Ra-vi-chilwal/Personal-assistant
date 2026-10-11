import time
from collections import defaultdict, deque
from typing import List, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.rag import ask

app = FastAPI(title="Ravindar Portfolio Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your portfolio domain when deploying
    allow_methods=["*"],
    allow_headers=["*"],
)

RATE_LIMIT = 15  # requests
RATE_WINDOW = 60  # seconds, per client IP
_hits = defaultdict(deque)


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=2000)


class Chat(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    history: List[Message] = Field(default_factory=list, max_length=12)


def rate_limit(request: Request):
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    q = _hits[ip]
    while q and now - q[0] > RATE_WINDOW:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        raise HTTPException(429, "Too many messages. Please wait a minute and try again.")
    q.append(now)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(body: Chat, request: Request):
    rate_limit(request)
    result = ask(body.question.strip(), [m.model_dump() for m in body.history])
    return {"answer": result["answer"]}
