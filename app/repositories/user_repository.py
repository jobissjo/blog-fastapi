from datetime import datetime

from bson import ObjectId
from app.core.db_config import db
from app.schemas.user_schema import RegisterUserSchema


class UserRepository:
    def __init__(self):
        self.collection = db.users

    async def create_user(self, user: RegisterUserSchema):
        return await self.collection.insert_one(
            {
                **user.model_dump(),
                "is_active": True,
                "join_date": datetime.now(),
                "profile": {
                    "bio": None,
                    "profile_picture": None,
                    "cover_picture": None,
                    "resume": None,
                },
            }
        )

    async def get_user_by_email(self, email: str):
        user_response = await self.collection.find_one({"email": email})
        if user_response is None:
            return None
        return user_response

    async def update_user_profile_picture(self, user_id: str, profile_picture_url: str):
        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"profile.profile_picture": profile_picture_url}},
        )

    async def update_user_password(self, user_id: str, password: str):
        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": password}},
        )
