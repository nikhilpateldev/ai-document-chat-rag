# AI Document Chat RAG

An AI-powered document chat system using FastAPI, Qdrant, LLaMA (Ollama),
and Angular. Upload documents, store embeddings in a vector database,
and chat with context-aware memory.

## Stack
- Angular (Frontend)
- FastAPI (Backend)
- Qdrant (Vector DB)
- Ollama + LLaMA 3
- BGE Large Embeddings

## Run
```bash
docker-compose up --build
.venv\Scripts\activate
python -m uvicorn app.main:app --reload
```
