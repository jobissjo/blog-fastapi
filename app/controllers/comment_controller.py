from app.services.comment_service import CommentService
from app.schemas.user_comment_schema import AnonymousCommentCreateSchema


class CommentController:
    def __init__(self):
        self.comment_service = CommentService()

    async def create_comment(
        self, blog_id: str, visitor_id: str, payload: AnonymousCommentCreateSchema
    ):
        return await self.comment_service.create_comment(blog_id, visitor_id, payload)

    async def list_comments(self, blog_id: str, limit: int = 50):
        return await self.comment_service.list_comments(blog_id, limit)