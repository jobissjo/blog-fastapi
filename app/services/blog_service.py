from app.repositories.blog_repository import BlogRepository
from app.schemas.user_schema import UserTokenDecodedData
from typing import Optional
from app.schemas.common import BaseResponseSchema

class BlogService:
    
    def __init__(self):
        self.repository = BlogRepository()

    def create_blog(self, token: UserTokenDecodedData, blog):
        self.repository.create_blog(token, blog)
        return BaseResponseSchema(success=True, message="Blog created successfully")
    
    def your_blogs(self, token: UserTokenDecodedData, published: Optional[bool] = None):
        return self.repository.get_all_blogs(user_id=token.id, published=published)
    
    def your_blog_by_id(self, token: UserTokenDecodedData, blog_id: str):
        return self.repository.get_blog_by_id(blog_id, token.id)
    
    def all_blogs(self, is_paginated: bool = False, skip: int = 1,  limit: int = 10):
        return self.repository.get_all_blogs(is_paginated, skip, limit, published=True)
    
    def blog_details(self, blog_id: str):
        return self.repository.get_blog_by_id(blog_id, published=True)
    
    def update_blog(self, token: UserTokenDecodedData, blog_id: str, blog):
        self.repository.update_blog(token, blog_id, blog)
        return BaseResponseSchema(success=True, message="Blog updated successfully")
    
    def delete_blog(self, token: UserTokenDecodedData, blog_id: str):
        self.repository.delete_blog(token, blog_id)
        return BaseResponseSchema(success=True, message="Blog deleted successfully")