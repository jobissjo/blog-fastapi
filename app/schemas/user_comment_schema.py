from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import BaseResponseSchema, PyObjectId


class AnonymousCommentCreateSchema(BaseModel):
    name: Optional[str] = Field(
        default=None,
        max_length=60,
        description="Display name for the anonymous comment",
    )
    comment: str = Field(..., min_length=1, max_length=2000)


class CommentResponseSchema(BaseModel):
    id: PyObjectId = Field(alias="_id")
    blog_id: PyObjectId
    visitor_id: Optional[str] = None
    name: str
    comment: str
    created_at: str
    updated_at: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


class CommentListResponseSchema(BaseResponseSchema):
    data: List[CommentResponseSchema]
    total: int


class CommentMutationResponseSchema(BaseResponseSchema):
    data: CommentResponseSchema