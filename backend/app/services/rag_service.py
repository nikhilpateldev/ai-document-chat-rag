from app.services.hybrid_retrieval import hybrid_search
from app.vectorstore.qdrant_store import QdrantStore
from app.services.llm_service import stream_generate_answer
from app.services.llm_service import generate_answer, build_prompt
from app.services.chat_memory_service import ChatMemoryService
from app.services.prompt_builder import format_chat_history
from app.services.context_builder import build_context_with_sources
from app.services.source_parser import extract_source_ids
from app.services.reranker_service import EmbeddingReranker
from app.services.embedding_service import EmbeddingService

reranker = EmbeddingReranker()
memory = ChatMemoryService()
qdrant_store = QdrantStore()
embedding_service = EmbeddingService()

def rag_answer(question: str, top_k: int = 5) -> dict:
    search_results = qdrant_store.search(question, top_k)

    if not search_results:
        return {
            "answer": "I don't know based on the provided documents.",
            "sources": []
        }

    context = "\n\n".join([
        f"- {hit['text']}" for hit in search_results
    ])

    answer = generate_answer(context, question)

    return {
        "answer": answer,
        "sources": [
            {
                "document": hit["document"],
                "chunk_id": hit["chunk_id"],
                "score": hit["score"]
            }
            for hit in search_results
        ]
    }

def stream_rag_answer(conversation_id, question, top_k=5):
    history = memory.get_history(conversation_id)
    chat_history = format_chat_history(history)

    # 1️⃣ Embed query (nomic-embed-text)
    query_vector = embedding_service.embed_query(question)

    # 2️⃣ Hybrid recall (BM25 + vector)
    chunks = hybrid_search(
        query=question,
        query_vector=query_vector,
        vector_k=20,
        bm25_k=20
    )

    # 3️⃣ Re-rank (precision)
    # chunks = reranker.rerank(
    #     query_vector=query_vector,
    #     chunks=chunks,
    #     top_n=top_k
    # )

    # 4️⃣ Build context from BEST chunks
    context, source_map = build_context_with_sources(chunks)

    prompt = build_prompt(context, question, chat_history)

    memory.add_turn(conversation_id, "user", question)

    full_answer = ""
    for token in stream_generate_answer(prompt):
        full_answer += token
        yield token

    used_sources = extract_source_ids(full_answer)
    memory.add_turn(conversation_id, "assistant", full_answer)

    yield "\n\n[SOURCES]\n"
    for src in used_sources:
        chunk = source_map[src.strip("[]")]
        yield f"- {chunk['document']} (page {chunk['page']}, chunk {chunk['chunk_id']})\n"


