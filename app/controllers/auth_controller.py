from app.schemas.user_schema import RegisterUserSchema, LoginUserSchema
from app.services.user_service import UserService

class AuthController:
    def __init__(self):
        self.service = UserService()
    
    async def register_user(self, user: RegisterUserSchema):
        return await self.service.register_user(user)
    

    async def login_user(self, user: LoginUserSchema):
        return await self.service.login_user(user)