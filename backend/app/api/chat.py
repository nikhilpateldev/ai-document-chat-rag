from fastapi import APIRouter
from pydantic import BaseModel
from app.models.chat_stream_request import ChatStreamRequest
from app.services.embedding_service import EmbeddingService
from app.vectorstore.qdrant_store import QdrantStore
from app.services.rag_service import rag_answer
from fastapi.responses import StreamingResponse
from app.services.rag_service import stream_rag_answer
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter(prefix="/chat", tags=["Chat"])

store = QdrantStore()

class ChatRequest(BaseModel):
    question: str
    top_k: int = 5

@router.post("/search")
async def search_documents(request: ChatRequest):
    query_embedding = EmbeddingService.embed([request.question])[0]

    results = store.search(
        query_vector=query_embedding,
        limit=request.top_k
    )

    return {
        "question": request.question,
        "results": results
    }

@router.post("/ask")
def ask_question(request: ChatRequest):
    return rag_answer(request.question, request.top_k)


@router.post("/ask-stream")
async def ask_stream(request: ChatStreamRequest):

    async def event_generator():
        try:
            for token in stream_rag_answer(
                question=request.question,
                conversation_id=request.sessionId,
                top_k=request.top_k
            ):
                yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
                await asyncio.sleep(0)

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

