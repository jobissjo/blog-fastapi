from fastapi import APIRouter, Depends
from app.schemas.newsletter import NewsletterSubscribeSchema
from app.controllers.newsletter_controller import NewsletterController


router = APIRouter(prefix="/newsletter", tags=["Newsletter"])


@router.post("/subscribe")
async def subscribe_newsletter(data: NewsletterSubscribeSchema, controller: NewsletterController = Depends(NewsletterController)):
    return await controller.subscribe(data)


@router.get("/unsubscribe/{subscription_id}")
async def unsubscribe_newsletter(subscription_id: str, controller: NewsletterController = Depends(NewsletterController)):
    return await controller.unsubscribe(subscription_id)

