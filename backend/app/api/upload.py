from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_loader import DocumentLoader
from app.services.text_chunker import TextChunker
from app.services.embedding_service import EmbeddingService
from app.vectorstore.qdrant_store import QdrantStore
from app.vectorstore.bm25_store import BM25Store
from app.models.chunk import ChunkedDocument

router = APIRouter(prefix="/documents", tags=["Documents"])

qdrant = QdrantStore()
bm25 = BM25Store()
embedding_service = EmbeddingService()


@router.post("/upload", response_model=ChunkedDocument)
async def upload_document(file: UploadFile = File(...)):
    try:
        # 1️⃣ Load document text
        text = await DocumentLoader.load(file)

        # 2️⃣ Chunk text
        chunks = TextChunker.chunk_text(text)

        if not chunks:
            raise ValueError("No text chunks generated")

        # 3️⃣ Generate embeddings (nomic-embed-text)
        embeddings = embedding_service.embed_chunks(chunks)

        # 4️⃣ Store in Qdrant (vectors + metadata)
        qdrant.upsert_chunks(
            embeddings=embeddings,
            chunks=chunks,
            filename=file.filename
        )

        # 5️⃣ Store in BM25 (keyword search)
        for idx, chunk in enumerate(chunks):
            bm25.upsert_chunk(
                chunk_id=f"{file.filename}_{idx}",
                content=chunk.content,
                filename=file.filename,
                page=None  # add later if you extract pages
            )

        # 6️⃣ Return response (informational only)
        return ChunkedDocument(
            filename=file.filename,
            chunks=chunks
        )

    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
