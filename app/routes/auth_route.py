from fastapi import APIRouter, Depends

from app.controllers.auth_controller import AuthController
from app.schemas.user_schema import RegisterUserPayloadSchema, LoginUserSchema, TokenFinalResponseSchema, TokenResponseSchema, ChangePasswordSchema, UserTokenDecodedData
from app.schemas.common import BaseResponseSchema
from fastapi.security import OAuth2PasswordRequestForm
from app.services.common_service import CommonService


router = APIRouter(prefix="/auth", tags=["Auth"])


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

@router.post("/token")
async def get_token(
    data: OAuth2PasswordRequestForm = Depends(), 
    controller: AuthController = Depends(AuthController)
) -> TokenResponseSchema:
    response = await controller.login_user(LoginUserSchema(email=data.username, password=data.password))
    return response.data

@router.post('/change-password')
async def change_password(
    user_data: ChangePasswordSchema,
    user: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    controller: AuthController = Depends(AuthController)
) -> BaseResponseSchema:
    return await controller.change_password(user, user_data)

