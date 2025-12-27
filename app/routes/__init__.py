from fastapi import APIRouter

from app.routes.auth_route import router as auth_router
from app.routes.series_route import router as series_router
from app.routes.blog_route import router as blog_router
from app.routes.comment_route import router as comment_router
from app.routes.portfolio_routes import router as portfolio_router
from app.routes.email_setting_routes import router as email_setting_router

router = APIRouter(prefix='/api')
router.include_router(auth_router)  
router.include_router(series_router)  
router.include_router(blog_router)  
router.include_router(comment_router)
router.include_router(portfolio_router)
router.include_router(email_setting_router)