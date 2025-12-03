from app.core.db_config import db
from bson import ObjectId
from typing import List, Optional
from app.schemas.blog_schema import BlogCreateSchema, BlogResponseSchema
from datetime import datetime


class BlogRepository:
    def __init__(self):
        self.collection = db.blogs
        self.view_collection = db.blog_views

    async def create_blog(self, blog: BlogCreateSchema, user_id: str):
        await self.collection.insert_one(
            {
                **blog.model_dump(),
                "user_id": ObjectId(user_id),
                "series_id": ObjectId(blog.series_id) if blog.series_id else None,
                "view_count": 0,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
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
            result = (
                self.collection.find(query).skip(skip).limit(limit)
            )
        else:
            result = self.collection.find(query).limit(max_limit)
        results = []
        async for doc in result:
            results.append(BlogResponseSchema(**doc))
        return results

    async def get_blog_by_id(
        self, blog_id: str=None, user_id: str = None, published: Optional[bool] = None,
        blog_slug: str = None
    ) -> BlogResponseSchema | None:
        if blog_id:
            query = {"_id": ObjectId(blog_id)}
        if blog_slug:
            query = {"slug": blog_slug}
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
            {
                "$set": {
                    **blog.model_dump(),
                    "user_id": ObjectId(user_id),
                    "updated_at": datetime.now().isoformat(),
                }
            },
        )

    async def patch_blog(self, blog_id: str, user_id: str, updates: dict):
        if not updates:
            return
        updates_with_meta = {
            **updates,
            "updated_at": datetime.now().isoformat(),
        }
        await self.collection.update_one(
            {"_id": ObjectId(blog_id), "user_id": ObjectId(user_id)},
            {"$set": updates_with_meta},
        )

    async def increment_view_count(self, blog_slug: str, visitor_id: Optional[str] = None):
        blog = await self.collection.find_one({"slug": blog_slug})
        if not blog:
            return
        if visitor_id:
            existing = await self.view_collection.find_one(
                {"blog_slug": blog_slug, "visitor_id": visitor_id}
            )
            if existing:
                return
            await self.view_collection.insert_one(
                {
                    "blog_slug": blog_slug,
                    "visitor_id": visitor_id,
                    "viewed_at": datetime.now().isoformat(),
                }
            )
        await self.collection.update_one(
            {"_id": blog["_id"]},
            {
                "$inc": {"view_count": 1},
                "$set": {"updated_at": datetime.now().isoformat()},
            },
        )

    async def delete_blog(self, blog_id: str, user_id: str):
        await self.collection.delete_one(
            {"_id": ObjectId(blog_id), "user_id": ObjectId(user_id)}
        )
