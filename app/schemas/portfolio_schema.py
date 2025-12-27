from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List
from app.schemas.common import PyObjectId, BaseResponseSchema

class ContactUsToEmailSchema(BaseModel):
    contact_us_type: str
    email: str

class ContactUsToEmailResponseSchema(BaseModel):
    id: PyObjectId = Field(alias="_id")
    contact_us_type: str
    email: str
    created_at: datetime
    model_config = ConfigDict(populate_by_name=True)

class ContactUsSchema(BaseModel):
    name: str
    email: str
    subject: str
    message: str


class ContactUsResponseSchema(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    email: str
    subject: str
    message: str
    created_at: datetime

    model_config = ConfigDict(populate_by_name=True)

class ListContactUsResponseSchema(BaseResponseSchema):
    data: List[ContactUsResponseSchema]

class DetailContactUsResponseSchema(BaseResponseSchema):
    data: ContactUsResponseSchema

