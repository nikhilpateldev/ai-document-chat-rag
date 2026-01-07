import os
import uuid
from typing import List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

from app.core.config import settings

COLLECTION_NAME = "my_docs"
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


class QdrantStore:

    def __init__(self):
        self.client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            check_compatibility=False
        )
        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == COLLECTION_NAME for c in collections):
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=768,  # nomic-embed-text
                    distance=Distance.COSINE
                )
            )

    def upsert_chunks(
        self,
        embeddings: List[List[float]],
        chunks: List[str],
        filename: str,
        pages: Optional[List[int]] = None
    ):
        """
        pages: optional list of page numbers aligned with chunks
        """

        points = []

        for idx, vector in enumerate(embeddings):
            chunk_id = str(uuid.uuid4())

            points.append(
                PointStruct(
                    id=chunk_id,
                    vector=vector,
                    payload={
                        "document_id": filename,
                        "filename": filename,
                        "chunk_id": chunk_id,
                        "chunk_index": idx,
                        "page": pages[idx] if pages else None,
                        "content": chunks[idx],
                        "vector":vector,
                    }
                )
            )

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )

    def search(self, query_vector: List[float], limit: int = 20):
        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True   # 👈 important
        )

        return [
                    {
                        "score": point.score,

                        # 👇 actual text content (nested)
                        "content": point.payload.get("content", {}).get("content"),

                        "document_id": point.payload.get("document_id"),
                        "filename": point.payload.get("filename"),
                        "page": point.payload.get("page"),
                        "chunk_id": point.payload.get("chunk_id"),
                        "chunk_index": point.payload.get("chunk_index"),
                        "vector": point.payload.get("vector")
                    }
                    for point in results.points
                ]


