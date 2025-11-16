from app.core.db_config import db
from bson import ObjectId
from typing import List, Optional
from app.schemas.blog_schema import BlogCreateSchema, BlogResponseSchema


class BlogRepository:
    def __init__(self):
        self.collection = db.blogs

    async def create_blog(self, blog: BlogCreateSchema):
        await self.collection.insert_one(
            {**blog.model_dump(), "user_id": ObjectId(blog.user_id)}
        )

    async def get_all_blogs(
        self,
        is_paginate: bool = False,
        skip: int = 0,
        limit: int = 10,
        user_id: str = None,
        search: str = None,
        series_id: str = None,
        max_limit: int = 100,
        published: Optional[bool] = None,
    ) -> List[BlogResponseSchema]:
        query = {}
        if user_id:
            query.update({"user_id": ObjectId(user_id)})

        if search:
            query.update(
                {
                    "$or": [
                        {"title": {"$regex": search, "$options": "i"}},
                        {"content": {"$regex": search, "$options": "i"}},
                    ]
                }
            )

        if series_id:
            query.update({"series_id": ObjectId(series_id)})

        if published is not None:
            query.update({"published": published})

        if is_paginate:
            return (
                await self.collection.find(query).skip(skip).limit(limit).to_list(limit)
            )
        else:
            return await self.collection.find(query).to_list(max_limit)

    async def get_blog_by_id(
        self, blog_id: str, user_id: str = None, published: Optional[bool] = None
    ) -> BlogResponseSchema | None:
        query = {"_id": ObjectId(blog_id)}
        if user_id:
            query.update({"user_id": ObjectId(user_id)})
        if published is not None:
            query.update({"published": published})
        response = await self.collection.find_one(query)
        if not response:
            return None
        return BlogResponseSchema(**response)

    async def update_blog(self, blog_id: str, user_id: str, blog: BlogCreateSchema):
        await self.collection.update_one(
            {"_id": ObjectId(blog_id), "user_id": ObjectId(user_id)},
            {"$set": {**blog.model_dump(), "user_id": ObjectId(user_id)}},
        )

    async def delete_blog(self, blog_id: str, user_id: str):
        await self.collection.delete_one(
            {"_id": ObjectId(blog_id), "user_id": ObjectId(user_id)}
        )
