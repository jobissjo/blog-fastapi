from app.core.db_config import db
from bson.objectid import ObjectId


class SeriesRepository:
    def __init__(self):
        self.collection = db.series

    def create_series(self, series, user_id: str)->None:
        self.collection.insert_one(series)

    def get_all_series(self, user_id: str = None, skip: int = 0, limit: int = 10):
        query = {}
        if user_id:
            query = {"user_id": ObjectId(user_id)}
        return self.collection.find(query).skip(skip).limit(limit)

    def get_series_by_id(self, series_id: str):
        return self.collection.find_one({"_id": ObjectId(series_id)})

    def update_series(self, user_id: str, series_id: str, series)->None:
        self.collection.update_one(
            {"_id": ObjectId(series_id), "user_id": ObjectId(user_id)}, {"$set": series}
        )

    def delete_series(self, user_id: str, series_id: str)->None:
        self.collection.delete_one(
            {"_id": ObjectId(series_id), "user_id": ObjectId(user_id)}
        )
