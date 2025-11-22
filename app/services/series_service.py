from app.repositories.series_repository import SeriesRepository
from app.schemas.common import BaseResponseSchema
from app.schemas.series_schema import SeriesCreateSchema, SeriesUpdateSchema
from fastapi import HTTPException
from app.schemas.user_schema import UserTokenDecodedData
from typing import Optional, List
from app.schemas.series_schema import (
    SeriesListResponseSchema,
    SeriesDetailResponseSchema,
)


class SeriesService:
    def __init__(self):
        self.repository = SeriesRepository()

    async def create_series(self, series: SeriesCreateSchema, user_id: str):
        await self.repository.create_series(series, user_id)
        return BaseResponseSchema(
            success=True, message="Series created successfully", data=None
        )

    async def get_all_series(
        self, skip: int = 0, limit: int = 10, search: Optional[str] = None
    ) -> SeriesListResponseSchema:
        response = await self.repository.get_all_series(
            skip, limit, search=search, published=True
        )
        return SeriesListResponseSchema(
            success=True, message="Series fetched successfully", data=response
        )

    async def get_your_series(
        self, user_id: str, skip: int = 0, limit: int = 10, search: Optional[str] = None,
        published:Optional[bool] = None
    ) -> SeriesListResponseSchema:
        response = await self.repository.get_all_series(
            skip, limit, user_id=user_id, search=search, published=published
        )
        return SeriesListResponseSchema(
            success=True, message="Series fetched successfully", data=response
        )

    async def get_series_by_id(self, series_id: str) -> SeriesDetailResponseSchema:
        response_data = await self.repository.get_series_by_id(series_id)
        return SeriesDetailResponseSchema(
            success=True, message="Series fetched successfully", data=response_data
        )

    async def get_series_by_slug(self, series_slug: str) -> SeriesDetailResponseSchema:
        response_data = await self.repository.get_series_by_id(series_slug=series_slug)
        return SeriesDetailResponseSchema(
            success=True, message="Series fetched successfully", data=response_data
        )

    async def update_series(
        self, user_id: str, series_id: str, series: SeriesUpdateSchema
    ):
        series_response = await self.repository.get_series_by_id(series_id)
        if series_response is None:
            raise HTTPException(status_code=404, detail="Series not found")
        await self.repository.update_series(user_id, series_id, series)
        return BaseResponseSchema(
            success=True, message="Series updated successfully", data=None
        )

    async def delete_series(self, user_id: str, series_id: str):
        series_response = await self.repository.get_series_by_id(series_id)
        if series_response is None:
            raise HTTPException(status_code=404, detail="Series not found")
        return await self.repository.delete_series(user_id, series_id)
