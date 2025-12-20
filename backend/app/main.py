from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(health_router)
app.include_router(upload_router)
