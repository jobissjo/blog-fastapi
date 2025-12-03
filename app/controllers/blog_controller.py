from typing import Optional
from app.services.blog_service import BlogService
from app.schemas.user_schema import UserTokenDecodedData
from app.schemas.blog_schema import BlogCreateFileSchema, BlogUpdateSchema

class BlogController:
    def __init__(self):
        self.service = BlogService()
    
    async def create_blog(self, token: UserTokenDecodedData, blog: BlogCreateFileSchema):
        return await self.service.create_blog(token, blog)
    
    async def your_blogs(self, token: UserTokenDecodedData):
        return await self.service.your_blogs(token)
    
    async def your_blog_by_id(self, token: UserTokenDecodedData, blog_id: str):
        return await self.service.your_blog_by_id(token, blog_id)
    
    async def all_blogs(self, is_paginated: bool = False, skip: int = 1, limit: int = 10):
        return await self.service.all_blogs(is_paginated, skip, limit)
    
    async def blog_details(self, blog_id: str, visitor_id: Optional[str] = None):
        return await self.service.blog_details(blog_id, visitor_id)

    async def update_blog(self, token: UserTokenDecodedData, blog_id: str, blog: BlogCreateFileSchema):
        return await self.service.update_blog(token, blog_id, blog)

    async def patch_blog(self, token: UserTokenDecodedData, blog_id: str, blog: BlogUpdateSchema):
        return await self.service.patch_blog(token, blog_id, blog)

    async def delete_blog(self, token: UserTokenDecodedData, blog_id: str):
        await self.service.delete_blog(token, blog_id)