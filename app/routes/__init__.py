from fastapi import APIRouter

from app.routes.auth_route import router as auth_router
from app.routes.series_route import router as series_router
from app.routes.blog_route import router as blog_router

router = APIRouter(prefix='/api')
router.include_router(auth_router)  
router.include_router(series_router)  
router.include_router(blog_router)  