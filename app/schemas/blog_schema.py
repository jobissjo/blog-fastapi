from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.common import PyObjectId
from bson import ObjectId
from fastapi import Form, File, UploadFile
from app.schemas.user_schema import UserBasicSchema


class BlogCreateFileSchema:
    def __init__(
        self,
        title: str = Form(...),
        slug: str = Form(...),
        content: str = Form(...),
        published: bool = Form(False),
        tags: List[str] = Form(default_factory=list),
        series_id: Optional[str] = Form(None),
        thumbnail: Optional[UploadFile] = File(None)
    ):
        self.title = title
        self.slug = slug
        self.content = content
        self.published = published
        self.tags = tags
        self.series_id = series_id
        self.thumbnail = thumbnail


class BlogCreateSchema(BaseModel):
    title: str
    slug: str
    content: str
    thumbnail: str
    published: bool = False
    tags: List[str] = Field(default_factory=list)
    series_id: Optional[str] = None
    view_count: int = 0

    

class BlogUpdateSchema(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    thumbnail: Optional[str] = None
    published: Optional[bool] = None
    tags: Optional[List[str]] = None
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
    series_id: Optional[PyObjectId] = None
    likes: Optional[int] = 0
    view_count: int = 0
    liked: Optional[bool] = False
    user_id: Optional[PyObjectId] = None
    user_details: Optional[UserBasicSchema] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str})

class BlogDetailResponseSchema(BaseModel):
    data: BlogResponseSchema
    success: bool
    message: str

class BlogListResponseSchema(BaseModel):
    data: List[BlogResponseSchema]
    total: int
    success: bool
    message: str