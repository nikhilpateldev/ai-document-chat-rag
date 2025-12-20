from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_loader import DocumentLoader
from app.models.document import ParsedDocument

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=ParsedDocument)
async def upload_document(file: UploadFile = File(...)):
    try:
        content = await DocumentLoader.load(file)
        return ParsedDocument(
            filename=file.filename,
            content=content
        )
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
