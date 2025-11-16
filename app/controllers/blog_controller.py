from app.services.blog_service import BlogService
from app.schemas.user_schema import UserTokenDecodedData
from app.schemas.blog_schema import BlogCreateSchema

class BlogController:
    def __init__(self):
        self.service = BlogService()
    
    def create_blog(self, token: UserTokenDecodedData, blog: BlogCreateSchema):
        return self.service.create_blog(token, blog)
    
    def your_blogs(self, token: UserTokenDecodedData):
        return self.service.your_blogs(token)
    
    def your_blog_by_id(self, token: UserTokenDecodedData, blog_id: str):
        return self.service.your_blog_by_id(token, blog_id)
    
    def all_blogs(self, is_paginated: bool = False, skip: int = 1, limit: int = 10):
        return self.service.all_blogs(is_paginated, skip, limit)
    
    def blog_details(self, blog_id: str):
        return self.service.blog_details(blog_id)

    def update_blog(self, token: UserTokenDecodedData, blog_id: str, blog: BlogCreateSchema):
        return self.service.update_blog(token, blog_id, blog)
    
    def delete_blog(self, token: UserTokenDecodedData, blog_id: str):
        self.service.delete_blog(token, blog_id)