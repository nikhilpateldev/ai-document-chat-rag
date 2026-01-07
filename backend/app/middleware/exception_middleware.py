import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("global-exception")

async def exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        logger.exception(
            "🔥 Unhandled exception",
            extra={
                "path": request.url.path,
                "method": request.method
            }
        )
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error"}
        )
