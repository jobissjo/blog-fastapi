from fastapi import APIRouter, Depends, Query, Request, Response

from app.controllers.comment_controller import CommentController
from app.schemas.user_comment_schema import AnonymousCommentCreateSchema
from app.utils.visitor import get_or_set_visitor_id

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/{blog_id}")
async def list_blog_comments(
    blog_id: str,
    limit: int = Query(50, le=100),
    controller: CommentController = Depends(CommentController),
):
    return await controller.list_comments(blog_id, limit)


@router.post("/{blog_id}")
async def create_blog_comment(
    blog_id: str,
    payload: AnonymousCommentCreateSchema,
    request: Request,
    response: Response,
    controller: CommentController = Depends(CommentController),
):
    visitor_id = get_or_set_visitor_id(request, response)
    return await controller.create_comment(blog_id, visitor_id, payload)