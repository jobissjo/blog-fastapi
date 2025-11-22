from app.repositories.blog_repository import BlogRepository
from app.schemas.user_schema import UserTokenDecodedData
from typing import Optional
from app.schemas.common import BaseResponseSchema
from app.services.cloudinary_service import CloudinaryService
from app.services.common_service import CommonService
from app.schemas.blog_schema import BlogCreateFileSchema, BlogCreateSchema


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
        )
        await self.repository.create_blog(blog_data, token.id)
        return BaseResponseSchema(success=True, message="Blog created successfully")

    async def your_blogs(self, token: UserTokenDecodedData, published: Optional[bool] = None):
        return await self.repository.get_all_blogs(user_id=token.id, published=published)

    async def your_blog_by_id(self, token: UserTokenDecodedData, blog_id: str):
        return await self.repository.get_blog_by_id(blog_id, token.id)

    async def all_blogs(self, is_paginated: bool = False, skip: int = 1, limit: int = 10):
        return await self.repository.get_all_blogs(is_paginated, skip, limit, published=True)

    async def blog_details(self, blog_id: str):
        return await self.repository.get_blog_by_id(blog_id, published=True)

    async def update_blog(self, token: UserTokenDecodedData, blog_id: str, blog: BlogCreateFileSchema):
        self.repository.update_blog(token, blog_id, blog)
        return BaseResponseSchema(success=True, message="Blog updated successfully")

    async def delete_blog(self, token: UserTokenDecodedData, blog_id: str):
        await self.repository.delete_blog(token, blog_id)
        return BaseResponseSchema(success=True, message="Blog deleted successfully")
