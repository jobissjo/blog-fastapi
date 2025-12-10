from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema, PyObjectId


class BaseUserSchema(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    email: str = Field(..., alias="email")
    phone_number: str = Field(..., alias="phoneNumber")
    username: str = Field(..., alias="username")
    password: str = Field(..., alias="password")
    role: str = Field(..., alias="role")
    dark_mode: Optional[bool] = Field(default=False)

    model_config = ConfigDict(populate_by_name=True)


class RegisterUserSchema(BaseUserSchema):
    password: str = Field(..., alias="password")

class RegisterUserPayloadSchema(RegisterUserSchema):
    service_key: str

class LoginUserSchema(BaseModel):
    email: str
    password:str


class UserTokenDecodedData(BaseModel):
    id: str
    email: str
    username: str
    role: str

class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    is_admin: bool = Field(False, alias='isAdmin')

class TokenFinalResponseSchema(BaseResponseSchema):
    data: TokenResponseSchema


class UserBasicSchema(BaseModel):
    id: PyObjectId = Field(alias="_id")
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    email: str = Field(..., alias="email")
    phone_number: str = Field(..., alias="phoneNumber")
    username: str = Field(..., alias="username")
    role: str = Field(..., alias="role")

    model_config = ConfigDict(populate_by_name=True)