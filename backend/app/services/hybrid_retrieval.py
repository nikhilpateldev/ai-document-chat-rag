from app.vectorstore.qdrant_store import QdrantStore
from app.vectorstore.bm25_store import BM25Store

qdrant = QdrantStore()
bm25 = BM25Store()

def hybrid_search(
    query: str,
    query_vector,
    vector_k: int = 20,
    bm25_k: int = 20
):
    vector_hits = qdrant.search(
        query_vector=query_vector,
        limit=vector_k
    )

    bm25_hits = bm25.search(
        query=query,
        limit=bm25_k
    )

    # Merge + dedupe by chunk_id
    merged = {}

    for hit in vector_hits:
        merged[hit["chunk_id"]] = hit

    for hit in bm25_hits:
        if hit["chunk_id"] not in merged:
            merged[hit["chunk_id"]] = hit
        else:
            merged[hit["chunk_id"]]["bm25_score"] = hit["bm25_score"]

    return list(merged.values())
