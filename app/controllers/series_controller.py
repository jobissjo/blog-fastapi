from optparse import Option
from app.services.series_service import SeriesService
from app.schemas.user_schema import UserTokenDecodedData
from typing import Optional


class SeriesController:
    def __init__(self):
        self.service = SeriesService()

    async def create_series(self, series, token: UserTokenDecodedData):
        return await self.service.create_series(series, token.id)

    async def get_all_series(
        self, skip: int = 0, limit: int = 10, search: Optional[str] = None
    ):
        return await self.service.get_all_series(skip, limit, search)

    async def get_series_by_id(self, series_id: str):
        return await self.service.get_series_by_id(series_id)

    async def get_series_by_slug(self, series_slug: str):
        return await self.service.get_series_by_slug(series_slug)

    async def get_your_series(
        self,
        token: UserTokenDecodedData,
        skip: int = 0,
        limit: int = 10,
        search: Optional[str] = None,
        published:Optional[str] = None,
    ):
        return await self.service.get_your_series(token.id, skip, limit, search, published)

    async def update_series(self, token: UserTokenDecodedData, series_id: str, series):
        return await self.service.update_series(token.id, series_id, series)

    async def delete_series(self, token: UserTokenDecodedData, series_id: str):
        return await self.service.delete_series(token.id, series_id)
