from pydantic import BaseModel, Field, ConfigDict
from app.schemas.common import BaseResponseSchema
from typing import List
from app.schemas.common import PyObjectId
from typing import Optional
from bson.objectid import ObjectId

class BaseSeriesSchema(BaseModel):
    title: str
    slug: str
    description: str
    published:bool


class SeriesCreateSchema(BaseSeriesSchema):
    pass

class SeriesUpdateSchema(BaseSeriesSchema):
    pass


class SeriesPatchSchema(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    published: Optional[bool] = None


class SeriesResponseSchema(BaseSeriesSchema):
    id: PyObjectId = Field(alias="_id")
    created_at: Optional[str]
    updated_at: Optional[str]
    model_config = ConfigDict(populate_by_name=True, json_encoders={ObjectId: str})


class SeriesDetailResponseSchema(BaseResponseSchema):
    data: SeriesResponseSchema


class SeriesListResponseSchema(BaseResponseSchema):
    data: List[SeriesResponseSchema]
