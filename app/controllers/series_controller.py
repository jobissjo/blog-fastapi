from app.services.series_service import SeriesService
from app.schemas.user_schema import UserTokenDecodedData


class SeriesController:
    def __init__(self):
        self.service = SeriesService()

    def create_series(self, series, token: UserTokenDecodedData):
        return self.service.create_series(series, token)

    def get_all_series(
        self, token: UserTokenDecodedData, skip: int = 0, limit: int = 10
    ):
        return self.service.get_all_series(token.id, skip, limit)

    def get_series_by_id(self, series_id: str):
        return self.service.get_series_by_id(series_id)

    def update_series(self, token: UserTokenDecodedData, series_id: str, series):
        return self.service.update_series(token.id, series_id, series)

    def delete_series(self, token: UserTokenDecodedData, series_id: str):
        return self.service.delete_series(token.id, series_id)
