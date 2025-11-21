from typing import Optional
from fastapi import APIRouter, Depends
from app.controllers.series_controller import SeriesController
from app.schemas.series_schema import SeriesCreateSchema, SeriesUpdateSchema
from app.services.common_service import CommonService
from app.schemas.user_schema import UserTokenDecodedData

router = APIRouter(prefix="/series", tags=["Series"])


@router.post("/")
async def create_series(
    series: SeriesCreateSchema,
    controller: SeriesController = Depends(SeriesController),
    token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    return await controller.create_series(series, token)


@router.get("/")
async def get_all_series(
    controller: SeriesController = Depends(SeriesController),
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
):
    return await controller.get_all_series(skip, limit, search)


@router.get("/your")
async def get_your_series(
    controller: SeriesController = Depends(SeriesController),
    token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    published:Optional[bool] = None
):
    return await controller.get_your_series(
        token, skip, limit, search, published
    )


@router.get("/{series_id}")
async def get_series_by_id(
    series_id: str, controller: SeriesController = Depends(SeriesController)
):
    return await controller.get_series_by_id(series_id)


@router.put("/{series_id}")
async def update_series(
    series_id: str,
    series: SeriesUpdateSchema,
    token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    controller: SeriesController = Depends(SeriesController),
):
    return await controller.update_series(token, series_id, series)


@router.delete("/{series_id}")
async def delete_series(
    series_id:str,
    controller: SeriesController = Depends(SeriesController),
    token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    ):
    return await controller.delete_series(token, series_id)
