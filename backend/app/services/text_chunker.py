from typing import List
from app.models.chunk import TextChunk
from app.core.config import settings


class TextChunker:
    """
    Splits text into overlapping chunks.
    """

    @staticmethod
    def chunk_text(text: str) -> List[TextChunk]:
        chunk_size = settings.CHUNK_SIZE
        overlap = settings.CHUNK_OVERLAP

        words = text.split()
        chunks: List[TextChunk] = []

        start = 0
        index = 0

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words).strip()
            if chunk_text:
                chunks.append(
                    TextChunk(
                        index=index,
                        content=chunk_text
                    )
                )

            index += 1
            start += chunk_size - overlap

        return chunks
