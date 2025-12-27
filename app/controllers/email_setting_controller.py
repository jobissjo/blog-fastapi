from app.services.email_service import EmailService
from app.schemas.email_settings_schema import EmailSettingsSchema


class EmailSettingController:
    def __init__(self):
        self.service = EmailService()
    
    async def create_email_settings(self, email_settings: EmailSettingsSchema):
        return await self.service.create_email_settings(email_settings)
    
    async def get_email_settings(self):
        return await self.service.get_email_settings()