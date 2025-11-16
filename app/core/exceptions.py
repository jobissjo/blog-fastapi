from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.core.logger_config import logger



async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.detail} in {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Generic Exception: {exc} in {request.url}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": f"{exc}"
        },
    )
