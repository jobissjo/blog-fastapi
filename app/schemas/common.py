from pydantic import BaseModel
from bson.objectid import ObjectId
from typing import Optional
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue

class BaseResponseSchema(BaseModel):
    success: bool
    message: str

class VisitorSchema(BaseModel):
    visitor_id: str

class VisitorResponseSchema(BaseResponseSchema):
    data: VisitorSchema

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if isinstance(v, ObjectId):
            return str(v)
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(str(v))

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        schema = handler(core_schema)
        schema.update(type="string")  
        return schema