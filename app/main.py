
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import settings_config as settings
from app.core.exceptions import http_exception_handler, generic_exception_handler
from fastapi.exceptions import HTTPException
from app.routes import router
from app.schemas.common import BaseResponseSchema

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS.split(","),
    allow_headers=settings.CORS_HEADERS.split(","),
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

@app.get("/")
async def read_root():
    return BaseResponseSchema(success=True, message='Welcome to Personal Blog')

app.include_router(router)
