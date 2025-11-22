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

    async def get_all_series(self,  skip: int = 0, limit: int = 10, user_id: str = None, search: str = None, published:str=None)->List[SeriesResponseSchema]:
        query = {}
        if user_id:
            query.update({"user_id": ObjectId(user_id)})
        if search:
            query.update({"$or": [{"title": {"$regex": search, "$options": "i"}}, {"description": {"$regex": search, "$options": "i"}}]})
        if published is not None:
            query.update({"published": published})

        if query:
            result  = self.collection.find(query).skip(skip).limit(limit)
        else:
            result = self.collection.find().skip(skip).limit(limit)
        results = []
        async for document in result:
            results.append(SeriesResponseSchema(**document))
        return results

    async def get_series_by_id(self, series_id: str=None, series_slug: str=None)->SeriesResponseSchema:
        if series_id:
            return SeriesResponseSchema(**await self.collection.find_one({"_id": ObjectId(series_id)}))
        elif series_slug:
            return SeriesResponseSchema(**await self.collection.find_one({"slug": series_slug}))

    async def update_series(self, user_id: str, series_id: str, series: SeriesCreateSchema)->None:
        await self.collection.update_one(
            {"_id": ObjectId(series_id), "user_id": ObjectId(user_id)},
            {
                "$set": {
                    **series.model_dump(),
                    "updated_at": datetime.now().isoformat(),
                }
            },
        )

    async def patch_series(self, user_id: str, series_id: str, updates: dict)->None:
        if not updates:
            return
        updates_with_meta = {
            **updates,
            "updated_at": datetime.now().isoformat(),
        }
        await self.collection.update_one(
            {"_id": ObjectId(series_id), "user_id": ObjectId(user_id)},
            {"$set": updates_with_meta},
        )

    async def delete_series(self, user_id: str, series_id: str)->None:
        await self.collection.delete_one(
            {"_id": ObjectId(series_id), "user_id": ObjectId(user_id)}
        )
