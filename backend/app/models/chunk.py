from pydantic import BaseModel
from typing import List

class TextChunk(BaseModel):
    index: int
    content: str

class ChunkedDocument(BaseModel):
    filename: str
    chunks: List[TextChunk]
