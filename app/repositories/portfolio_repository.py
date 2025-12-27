from app.core.db_config import db
from app.schemas.portfolio_schema import ContactUsSchema, ContactUsResponseSchema, ContactUsToEmailSchema, ContactUsToEmailResponseSchema
from bson.objectid import ObjectId
from datetime import datetime
from typing import List


class PortfolioRepository:
    def __init__(self):
        self.contact_us_collection = db.contact_us
        self.contact_us_to_collection = db.contact_us_to_email

    async def create_contact_us(self, contact_us: ContactUsSchema):
        await self.contact_us_collection.insert_one(
            {**contact_us.model_dump(), "created_at": datetime.now()}
        )

    async def get_contact_us(
        self, skip: int = 1, limit: int = 10
    ) -> List[ContactUsResponseSchema]:
        results = self.contact_us_collection.find().skip(skip).limit(limit)
        response = []
        async for result in results:
            response.append(ContactUsResponseSchema(**result))
        return response

    async def get_contact_us_by_id(self, contact_us_id: str) -> ContactUsResponseSchema:
        result = await self.contact_us_collection.find_one(
                {"_id": ObjectId(contact_us_id)}
            )
        if not result:
            return None
        return ContactUsResponseSchema(**result)

    async def create_contact_us_to(self, contact_us: ContactUsToEmailSchema):
        await self.contact_us_to_collection.insert_one(
            {**contact_us.model_dump(), "created_at": datetime.now()}
        )
    
    async def get_contact_us_to_by_type(self, contact_us_type: str)->ContactUsToEmailResponseSchema|None:
        results = await self.contact_us_to_collection.find_one(
            {"contact_us_type": contact_us_type}
        )
        if not results:
            return None
        return ContactUsToEmailResponseSchema(**results)