from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.core.config import settings
from app.api.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging
from app.middleware.exception_middleware import exception_middleware
from app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler
)
setup_logging()
app = FastAPI(title=settings.APP_NAME)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(exception_middleware)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)