from datetime import datetime
from typing import List

from bson import ObjectId

from app.core.db_config import db
from app.schemas.user_comment_schema import (
    AnonymousCommentCreateSchema,
    CommentResponseSchema,
)

class CommentRepository:
    def __init__(self):
        self.collection = db.comments
    
    async def create_comment(
        self,
        blog_id: str,
        visitor_id: str,
        comment: AnonymousCommentCreateSchema,
    ) -> CommentResponseSchema:
        payload = {
            "blog_id": ObjectId(blog_id),
            "visitor_id": visitor_id,
            "name": comment.name or "Anonymous",
            "comment": comment.comment,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        inserted = await self.collection.insert_one(payload)
        payload["_id"] = inserted.inserted_id
        return CommentResponseSchema(**payload)

    async def get_comments_by_blog(
        self, blog_id: str, limit: int = 50
    ) -> List[CommentResponseSchema]:
        cursor = (
            self.collection.find({"blog_id": ObjectId(blog_id)})
            .sort("created_at", -1)
            .limit(limit)
        )
        comments = []
        async for doc in cursor:
            comments.append(CommentResponseSchema(**doc))
        return comments