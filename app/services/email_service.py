from app.repositories.email_settings_repository import EmailSettingsRepository
from app.schemas.email_settings_schema import EmailSettingsSchema, ListEmailSettingResponseSchema
from fastapi.exceptions import HTTPException
from app.utils.common import render_email_template
from email.message import EmailMessage
import ssl
import aiosmtplib
from app.core.logger_config import logger
from app.schemas.common import BaseResponseSchema

class EmailService:
    def __init__(self):
        self.repository = EmailSettingsRepository()

    async def create_email_settings(self, email_settings: EmailSettingsSchema):
        await self.repository.create_email_settings(email_settings)
        return BaseResponseSchema(
            success=True,
            message="Email settings created successfully",
        )

    async def get_email_settings(self)->ListEmailSettingResponseSchema:
        data = await self.repository.get_email_settings()
        return ListEmailSettingResponseSchema(
            data=data, success=True, message="Email settings created successfully"
        )

    async def send_email(self, email: str, subject: str, body: dict, template_name:str):
        email_setting = await self.repository.get_active_email_settings()
        if not email_setting:
            raise HTTPException(status_code=404, detail="Email settings not found")
        
        try:
            email_body = await render_email_template(template_name, body)
        

            message = EmailMessage()
            message["From"] = email_setting.smtp_username
            message["To"] = email
            message["Subject"] = subject
            message.set_content(email_body, subtype="html")

            context = ssl.create_default_context()

            await aiosmtplib.send(
                message,
                hostname=email_setting.smtp_host,
                port=email_setting.smtp_port,
                username=email_setting.smtp_username,
                password=email_setting.smtp_password,
                start_tls=True,
                tls_context=context,
            )
        except Exception as e:
            logger.error(f"Email send failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

