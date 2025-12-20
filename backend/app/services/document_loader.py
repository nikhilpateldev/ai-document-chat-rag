from pypdf import PdfReader
from docx import Document as DocxDocument
from fastapi import UploadFile
import io

class DocumentLoader:

    @staticmethod
    async def load(file: UploadFile) -> str:
        filename = file.filename.lower()

        if filename.endswith(".pdf"):
            return DocumentLoader._load_pdf(await file.read())

        if filename.endswith(".docx"):
            return DocumentLoader._load_docx(await file.read())

        if filename.endswith(".txt"):
            return (await file.read()).decode("utf-8")

        raise ValueError("Unsupported file type")

    @staticmethod
    def _load_pdf(data: bytes) -> str:
        reader = PdfReader(io.BytesIO(data))
        text = []
        for page in reader.pages:
            if page.extract_text():
                text.append(page.extract_text())
        return "\n".join(text)

    @staticmethod
    def _load_docx(data: bytes) -> str:
        doc = DocxDocument(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
