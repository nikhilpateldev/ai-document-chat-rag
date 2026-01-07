import httpx
from typing import List
from app.core.config import settings
from app.models.chunk import TextChunk


class EmbeddingService:

    @staticmethod
    def embed_chunks(chunks: list[TextChunk]) -> list[list[float]]:
        embeddings = []

        for chunk in chunks:
            response = httpx.post(
                f"{settings.OLLAMA_URL}/api/embed",
                json={
                    "model": "nomic-embed-text",
                    "input": chunk.content  # ✅ STRING
                },
                timeout=60
            )

            response.raise_for_status()
            embeddings.append(response.json()["embeddings"][0])

        return embeddings
    
    @staticmethod
    def embed_query(input: str) -> list[float]:

        response = httpx.post(
                    f"{settings.OLLAMA_URL}/api/embed",
                    json={
                        "model": "nomic-embed-text",
                        "input": input  # ✅ STRING
                    },
                    timeout=60
                )

        response.raise_for_status()

        return response.json()["embeddings"][0]

