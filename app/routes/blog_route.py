from fastapi import APIRouter, Depends
from app.services.common_service import CommonService
from app.schemas.user_schema import UserTokenDecodedData
from app.controllers.blog_controller import BlogController
from app.schemas.blog_schema import  BlogCreateFileSchema

router = APIRouter(prefix="/blog", tags=["Blog"])


@router.post("/")
async def create_blog(
    blog: BlogCreateFileSchema = Depends(BlogCreateFileSchema),
    token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    controller: BlogController = Depends(BlogController),
):
    return await controller.create_blog(token, blog)


@router.get("/your")
async def get_your_blogs(
    token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    controller: BlogController = Depends(BlogController),
):
    return controller.your_blogs(token)

@router.get("/your/{blog_id}")
async def get_your_blog_by_id(
    blog_id: str,
    token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    controller: BlogController = Depends(BlogController),
):
    return controller.your_blog_by_id(token, blog_id)


@router.get("/")
async def get_all_blogs(
    is_paginated: bool = False,
    skip: int = 1,
    limit: int = 10,
    controller: BlogController = Depends(BlogController),
):
    return controller.all_blogs(is_paginated, skip, limit)


@router.get("/{blog_id}")
async def get_blog_by_id(
    blog_id: str, controller: BlogController = Depends(BlogController)
):
    return controller.blog_details(blog_id)


@router.put("/{blog_id}")
async def update_blog(
    blog_id: str,
    blog: BlogCreateFileSchema = Depends(BlogCreateFileSchema),
    token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    controller: BlogController = Depends(BlogController),
):
    return controller.update_blog(token, blog_id, blog)


@router.delete("/{blog_id}")
async def delete_blog(
    blog_id: str,
    token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    controller: BlogController = Depends(BlogController),
):
    return controller.delete_blog(token, blog_id)
