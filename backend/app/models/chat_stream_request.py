# app/models/chat.py
from pydantic import BaseModel

class ChatStreamRequest(BaseModel):
    question: str
    sessionId: str
    top_k: int = 5
