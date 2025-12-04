from app.repositories.blog_repository import BlogRepository
from app.schemas.user_schema import UserTokenDecodedData
from typing import Optional
from app.schemas.common import BaseResponseSchema
from app.services.cloudinary_service import CloudinaryService
from app.schemas.blog_schema import (
    BlogCreateFileSchema,
    BlogCreateSchema,
    BlogUpdateSchema,
    BlogListResponseSchema,
    BlogDetailResponseSchema,
)
from fastapi import HTTPException

BLOG_NOT_FOUND_MESSAGE = "Blog not found"

class BlogService:
    def __init__(self):
        self.repository = BlogRepository()
        self.cloudinary_service = CloudinaryService()

    async def create_blog(
        self, token: UserTokenDecodedData, blog: BlogCreateFileSchema
    ):
        thumbnail = await self.cloudinary_service.upload_image(blog.thumbnail)
        thumbnail = thumbnail.get("url")
        blog_data = BlogCreateSchema(
            title=blog.title,
            slug=blog.slug,
            content=blog.content,
            thumbnail=thumbnail,
            published=blog.published,
            tags=blog.tags,
            series_id=blog.series_id,
            view_count=0,
        )
        await self.repository.create_blog(blog_data, token.id)
        return BaseResponseSchema(success=True, message="Blog created successfully")

    async def your_blogs(self, token: UserTokenDecodedData, published: Optional[bool] = None)->BlogListResponseSchema:
        data = await self.repository.get_all_blogs(user_id=token.id, published=published)
        return BlogListResponseSchema(data=data, total=len(data), success=True, message="Your blogs")

    async def your_blog_by_id(self, token: UserTokenDecodedData, blog_id: str)->BlogDetailResponseSchema:
        data = await self.repository.get_blog_by_id(blog_id, token.id)
        return BlogDetailResponseSchema(data=data, success=True, message="Blog details")

    async def all_blogs(self, is_paginated: bool = False, skip: int = 1, limit: int = 10)->BlogListResponseSchema:
        data = await self.repository.get_all_blogs(is_paginated, skip, limit, published=True)
        return BlogListResponseSchema(data=data, total=len(data), success=True, message="All blogs")

    async def blog_details(self, blog_slug: str, visitor_id: Optional[str] = None)->BlogDetailResponseSchema:
        data = await self.repository.get_blog_by_id(blog_slug=blog_slug, published=True)
        if not data:
            raise HTTPException(status_code=404, detail=BLOG_NOT_FOUND_MESSAGE)
        await self.repository.increment_view_count(blog_slug=blog_slug, visitor_id=visitor_id)
        updated_data = await self.repository.get_blog_by_id(blog_slug=blog_slug, published=True)
        is_liked = await self.repository.check_liked_blog(blog_id=data.id, visitor_id=visitor_id)
        print(  "is_liked:", is_liked)
        updated_data.liked = is_liked
        return BlogDetailResponseSchema(data=updated_data, success=True, message="Blog details")

    async def like_blog(self, blog_slug: str, visitor_id: Optional[str] = None):
        data = await self.repository.get_blog_by_id(blog_slug=blog_slug, published=True)
        if not data:
            raise HTTPException(status_code=404, detail=BLOG_NOT_FOUND_MESSAGE)
        await self.repository.add_like(blog_id=data.id, visitor_id=visitor_id)
        updated = await self.repository.get_blog_by_id(blog_slug=blog_slug, published=True)
        if not updated:
            raise HTTPException(status_code=404, detail=BLOG_NOT_FOUND_MESSAGE)
        return BlogDetailResponseSchema(data=updated, success=True, message="Blog liked")

    async def update_blog(self, token: UserTokenDecodedData, blog_id: str, blog: BlogCreateFileSchema):
        blog_instance = await self.repository.get_blog_by_id(blog_id, token.id)
        if not blog_instance:
            raise HTTPException(status_code=404, detail=BLOG_NOT_FOUND_MESSAGE)
        if blog.thumbnail:
            thumbnail = await self.cloudinary_service.upload_image(blog.thumbnail)
            thumbnail = thumbnail.get("url")
        else:
            thumbnail = blog_instance.thumbnail
        blog_data = BlogCreateSchema(
            title=blog.title,
            slug=blog.slug,
            content=blog.content,
            thumbnail=thumbnail,
            published=blog.published,
            tags=blog.tags,
            series_id=blog.series_id,
            view_count=blog_instance.view_count,
        )
        await self.repository.update_blog(blog_id, token.id, blog_data)
        blog_updated_instance = await self.repository.get_blog_by_id(blog_id, token.id)
        return BlogDetailResponseSchema(data=blog_updated_instance, success=True, message="Blog updated successfully")

    async def patch_blog(self, token: UserTokenDecodedData, blog_id: str, blog: BlogUpdateSchema):
        blog_instance = await self.repository.get_blog_by_id(blog_id, token.id)
        if not blog_instance:
            raise HTTPException(status_code=404, detail=BLOG_NOT_FOUND_MESSAGE)
        update_payload = blog.model_dump(exclude_none=True)
        update_payload.pop("view_count", None)
        if not update_payload:
            return BlogDetailResponseSchema(
                data=blog_instance,
                success=True,
                message="No changes supplied",
            )
        await self.repository.patch_blog(blog_id, token.id, update_payload)
        updated_blog = await self.repository.get_blog_by_id(blog_id, token.id)
        return BlogDetailResponseSchema(
            data=updated_blog,
            success=True,
            message="Blog updated successfully",
        )

    async def delete_blog(self, token: UserTokenDecodedData, blog_id: str):
        await self.repository.delete_blog(blog_id, token.id)
        return BaseResponseSchema(success=True, message="Blog deleted successfully")
