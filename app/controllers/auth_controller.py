from app.schemas.user_schema import RegisterUserSchema, LoginUserSchema, ChangePasswordSchema, UserTokenDecodedData
from app.services.user_service import UserService

class AuthController:
    def __init__(self):
        self.service = UserService()
    
    async def register_user(self, user: RegisterUserSchema):
        return await self.service.register_user(user)
    

    async def login_user(self, user: LoginUserSchema):
        return await self.service.login_user(user)

    async def change_password(self, user: UserTokenDecodedData, user_data: ChangePasswordSchema):
        return await self.service.change_password(user, user_data)