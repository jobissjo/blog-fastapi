from app.core.db_config import db
from app.schemas.email_settings_schema import EmailSettingsSchema, EmailSettingResponseSchema
from datetime import datetime
from typing import List

class EmailSettingsRepository:
    def __init__(self):
        self.collection = db.email_settings

    async def create_email_settings(self, email: EmailSettingsSchema):
        return await self.collection.insert_one(
            {
                **email.model_dump(),
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        )
    
    async def update_email_settings(self, email_id: str, email: EmailSettingsSchema):
        return await self.collection.update_one(
            {"_id": email_id},
            {"$set": {**email.model_dump(), "updated_at": datetime.now()}},
        )
    
    async def get_email_settings(self) -> List[EmailSettingResponseSchema]:
        result = self.collection.find()
        return [EmailSettingResponseSchema(**result) async for result in result]

    async def get_active_email_settings(self) -> EmailSettingResponseSchema | None:
        result = await self.collection.find_one({"is_active": True})
        if not result:
            return None
        return EmailSettingResponseSchema(**result)
