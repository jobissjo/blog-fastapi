
from app.repositories.newsletter_repository import NewsletterRepository
from app.schemas.newsletter import NewsletterSubscribeSchema
from app.schemas.common import BaseResponseSchema
class NewsletterService:
    def __init__(self):
        self.repository = NewsletterRepository()
    
    async def subscribe(self, data: NewsletterSubscribeSchema):
        already_subscribed = await self.repository.get_subscription_by_email(data.email)
        if already_subscribed:
            return BaseResponseSchema(
                success=False,
                message="Email already subscribed"
            )
        await self.repository.subscribe(data.model_dump())
        return BaseResponseSchema(
            success=True,
            message="Subscribed successfully"
        )
    
    async def unsubscribe(self, subscription_id):
        subscription = await self.repository.get_subscription_by_id(subscription_id)
        if not subscription:
            return BaseResponseSchema(
                success=False,
                message="Subscription not found"
            )
        await self.repository.unsubscribe(subscription_id)
        return BaseResponseSchema(
            success=True,
            message="Unsubscribed successfully"
        )
