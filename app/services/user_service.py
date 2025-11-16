from fastapi.exceptions import HTTPException
from app.core import settings_config as settings
from app.repositories.user_repository import UserRepository
from app.services.common_service import CommonService
from app.schemas.user_schema import (
    RegisterUserPayloadSchema,
    RegisterUserSchema,
    LoginUserSchema,
    TokenResponseSchema,
    TokenFinalResponseSchema,
)


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def register_user(self, user: RegisterUserPayloadSchema):
        email_exists = await self.repository.get_user_by_email(user.email)
        if email_exists:
            raise HTTPException(status_code=400, detail="Email already exists")
        hashed_password = await CommonService.hash_password(user.password)
        if user.service_key != settings.SERVICE_KEY:
            raise HTTPException(status_code=400, detail="Invalid service key")
        user.password = hashed_password
        user = await self.repository.create_user(
            RegisterUserSchema(**user.model_dump())
        )
        return {"success": True, "message": "User registered successfully"}

    async def login_user(self, user_data: LoginUserSchema):
        user = await self.repository.get_user_by_email(user_data.email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not await CommonService.verify_password(
            user_data.password, user["password"]
        ):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = await CommonService.create_access_token(
            {
                "id": str(user["_id"]),
                "email": user["email"],
                "username": user["username"],
                "role": user["role"],
            }
        )
        refresh_token = await CommonService.create_refresh_token({"id": str(user["_id"])})
        token_response = TokenResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            isAdmin=user["role"] == "admin",
        )
        return TokenFinalResponseSchema(
            data=token_response, success=True, message="User logged in successfully"
        )
