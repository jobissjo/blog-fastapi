
from app.services.newsletter_service import NewsletterService

class NewsletterController:
    def __init__(self):
        self.service = NewsletterService()
    
    async def subscribe(self, data):
        return await self.service.subscribe(data)
    
    async def unsubscribe(self, subscription_id):
        return await self.service.unsubscribe(subscription_id)
