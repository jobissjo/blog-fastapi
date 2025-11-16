from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    success: bool
    message: str