from app.repositories.comment_repository import CommentRepository
from app.schemas.user_comment_schema import (
    AnonymousCommentCreateSchema,
    CommentListResponseSchema,
    CommentMutationResponseSchema,
)


class CommentService:
    def __init__(self):
        self.comment_repository = CommentRepository()

    async def create_comment(
        self, blog_id: str, visitor_id: str, comment: AnonymousCommentCreateSchema
    ) -> CommentMutationResponseSchema:
        created = await self.comment_repository.create_comment(
            blog_id, visitor_id, comment
        )
        return CommentMutationResponseSchema(
            success=True,
            message="Comment added",
            data=created,
        )

    async def list_comments(
        self, blog_id: str, limit: int = 50
    ) -> CommentListResponseSchema:
        comments = await self.comment_repository.get_comments_by_blog(blog_id, limit)
        return CommentListResponseSchema(
            success=True,
            message="Comments fetched",
            data=comments,
            total=len(comments),
        )