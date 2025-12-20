from pydantic import BaseModel

class ParsedDocument(BaseModel):
    filename: str
    content: str
