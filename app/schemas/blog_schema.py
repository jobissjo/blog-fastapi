from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.common import PyObjectId
from bson import ObjectId

class BlogCreateSchema(BaseModel):
    title: str
    slug: str
    content: str
    thumbnail: str
    published: bool = False
    tags: List[str] = Field(default_factory=list)
    series_id: Optional[str] = None

    

class BlogResponseSchema(BaseModel):
    id: PyObjectId = Field(alias="_id")
    title: str
    slug: str
    content: str
    thumbnail: str
    published: bool
    created_at: str
    updated_at: str
    tags: List[str]
    series_id: Optional[str] = None
    likes: int

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str})
