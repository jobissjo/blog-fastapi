from app.core.db_config import db
from bson.objectid import ObjectId
from app.schemas.series_schema import SeriesResponseSchema, SeriesCreateSchema
from typing import List
from datetime import datetime

class SeriesRepository:
    def __init__(self):
        self.collection = db.series

    async def create_series(self, series: SeriesCreateSchema, user_id: str)->None:
        # Datetime is iso format
        await self.collection.insert_one({
            **series.model_dump(),
            "user_id": ObjectId(user_id),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        })

    async def get_all_series(self,  skip: int = 0, limit: int = 10, user_id: str = None, search: str = None)->List[SeriesResponseSchema]:
        query = {}
        if user_id:
            query = {"user_id": ObjectId(user_id)}
        if search:
            query = {"$or": [{"title": {"$regex": search, "$options": "i"}}, {"description": {"$regex": search, "$options": "i"}}]}
        if query:
            result  = self.collection.find(query).skip(skip).limit(limit)
        else:
            result = self.collection.find().skip(skip).limit(limit)
        results = []
        async for document in result:
            results.append(SeriesResponseSchema(**document))
        return results

    async def get_series_by_id(self, series_id: str)->SeriesResponseSchema:
        return SeriesResponseSchema(**await self.collection.find_one({"_id": ObjectId(series_id)}))

    async def update_series(self, user_id: str, series_id: str, series: SeriesCreateSchema)->None:
        await self.collection.update_one(
            {"_id": ObjectId(series_id), "user_id": ObjectId(user_id)}, {"$set": series.model_dump()}
        )

    def delete_series(self, user_id: str, series_id: str)->None:
        self.collection.delete_one(
            {"_id": ObjectId(series_id), "user_id": ObjectId(user_id)}
        )
