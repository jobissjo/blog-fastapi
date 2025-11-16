from fastapi import APIRouter, Depends

from app.controllers.auth_controller import AuthController
from app.schemas.user_schema import RegisterUserPayloadSchema, LoginUserSchema, TokenFinalResponseSchema
from app.schemas.common import BaseResponseSchema

router = APIRouter(prefix="/users", tags=["Auth"])


@router.post("/")
async def register_user(
    user: RegisterUserPayloadSchema, controller: AuthController = Depends(AuthController)
) -> BaseResponseSchema:
    return await controller.register_user(user)

@router.post("/login")
async def login_user(
    user: LoginUserSchema, controller: AuthController = Depends(AuthController)
) -> TokenFinalResponseSchema:
    return await controller.login_user(user)

