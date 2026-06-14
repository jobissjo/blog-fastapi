
from app.core.db_config import db

class NewsletterRepository:
    
    
    def __init__(self):
        self.collection = db.newsletters

    async def get_subscription_by_email(self, email):
        return await self.collection.find_one({"email": email})
    
    async def get_subscription_by_id(self, subscription_id):
        return await self.collection.find_one({"_id": subscription_id})
    
    async def subscribe(self, data):
        return await self.collection.insert_one(data)
    
    async def unsubscribe(self, subscription_id):
        return await self.collection.delete_one({"_id": subscription_id})

    async def get_all_subscriptions(self):
        return await self.collection.find()