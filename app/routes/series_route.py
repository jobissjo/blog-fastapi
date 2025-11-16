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
    return controller.create_series(series)


@router.get("/")
async def get_all_series(controller: SeriesController = Depends(SeriesController)):
    return controller.get_all_series()


@router.get("/{series_id}")
async def get_series_by_id(controller: SeriesController = Depends(SeriesController)):
    return controller.get_series_by_id()


@router.put("/{series_id}")
async def update_series(
    series_id: str,
    series: SeriesUpdateSchema,
    token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
    controller: SeriesController = Depends(SeriesController),
):
    return controller.update_series(series_id, series)


@router.delete("/{series_id}")
async def delete_series(controller: SeriesController = Depends(SeriesController)):
    return controller.delete_series()
