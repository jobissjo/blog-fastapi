from pydantic import BaseModel, Field
from app.schemas.common import PyObjectId
from typing import List
from datetime import datetime
from app.schemas.common import BaseResponseSchema


class EmailSettingsSchema(BaseModel):
    email_type: str
    email: str
    smtp_port: int
    smtp_password: str
    smtp_host: str
    smtp_username: str
    is_active: bool


class EmailSettingResponseSchema(EmailSettingsSchema):
    id: PyObjectId = Field(alias="_id")
    created_at: datetime
    updated_at: datetime


class ListEmailSettingResponseSchema(BaseResponseSchema):
    data: List[EmailSettingResponseSchema]


class DetailEmailSettingResponseSchema(BaseResponseSchema):
    data: EmailSettingResponseSchema
