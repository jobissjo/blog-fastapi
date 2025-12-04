
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.core import settings_config as settings
from app.core.exceptions import http_exception_handler, generic_exception_handler
from fastapi.exceptions import HTTPException
from app.routes import router
from app.schemas.common import BaseResponseSchema, VisitorResponseSchema, VisitorSchema

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

@app.get("/api/visitor_id")
async def health_check(request: Request,
    response: Response,):
    from app.utils.visitor import get_or_set_visitor_id
    visitor_id = get_or_set_visitor_id(request, response)
    data = VisitorSchema(visitor_id=visitor_id)
    response = VisitorResponseSchema(data=data, success=True, message="Visitor ID retrieved")
    return response


app.include_router(router)
