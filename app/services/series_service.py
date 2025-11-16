from app.repositories.series_repository import SeriesRepository
from app.schemas.series_schema import SeriesCreateSchema, SeriesUpdateSchema
from fastapi import HTTPException
from app.schemas.user_schema import UserTokenDecodedData

class SeriesService:
    def __init__(self):
        self.repository = SeriesRepository()

    def create_series(self, series: SeriesCreateSchema, user_id: str):
        return self.repository.create_series(series, user_id)

    def get_all_series(self, user_id: str, skip: int = 0, limit: int = 10):
        return self.repository.get_all_series(user_id, skip, limit)

    def get_series_by_id(self, series_id: str):
        return self.repository.get_series_by_id(series_id)

    def update_series(self, user_id: str, series_id: str, series: SeriesUpdateSchema):
        series_response = self.repository.get_series_by_id(series_id)
        if series_response is None:
            raise HTTPException(status_code=404, detail="Series not found")
        return self.repository.update_series(user_id, series_id, series)

    def delete_series(self, user_id: str, series_id: str):
        series_response = self.repository.get_series_by_id(series_id)
        if series_response is None:
            raise HTTPException(status_code=404, detail="Series not found")
        return self.repository.delete_series(user_id, series_id)
