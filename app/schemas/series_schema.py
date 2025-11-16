from pydantic import BaseModel, Field
from app.schemas.common import BaseResponseSchema
from typing import List
from app.schemas.common import PyObjectId


class BaseSeriesSchema(BaseModel):
    title: str
    slug: str
    description: str


class SeriesCreateSchema(BaseSeriesSchema):
    pass

class SeriesUpdateSchema(BaseSeriesSchema):
    pass


class SeriesResponseSchema(BaseSeriesSchema):
    id: PyObjectId = Field(alias="_id")
    created_at: str
    updated_at: str


class SeriesDetailResponseSchema(BaseResponseSchema):
    data: SeriesResponseSchema


class SeriesListResponseSchema(BaseResponseSchema):
    data: List[SeriesResponseSchema]
