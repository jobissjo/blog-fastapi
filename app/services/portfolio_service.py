from fastapi import HTTPException
from app.repositories.portfolio_repository import PortfolioRepository
from app.schemas.portfolio_schema import (
    ContactUsSchema,
    ListContactUsResponseSchema,
    DetailContactUsResponseSchema,
)
from app.schemas.common import BaseResponseSchema
from app.services.email_service import EmailService
from app.core.logger_config import logger
from app.utils.constants import CONTACT_US_TO_PORTFOLIO


class PortfolioService:
    def __init__(self):
        self.repository = PortfolioRepository()
        self.email_service = EmailService()

    async def create_contact_us(
        self, contact_us: ContactUsSchema
    ) -> BaseResponseSchema:
        await self.repository.create_contact_us(contact_us)
        contact_us_to = await self.repository.get_contact_us_to_by_type(
            CONTACT_US_TO_PORTFOLIO
        )
        # NO NEED TO BLOCKING CODE, RUN IN BACKGROUND or SEPARATE THREAD
        if contact_us_to:
            print("contact_us.email", contact_us_to.email)
            await self.email_service.send_email(
                email=contact_us_to.email,
                subject="Contact Us",
                body=contact_us.model_dump(),
                template_name="contact_us.html",
            )
            logger.info(f"Contact Us  email send to {contact_us.email} successfully")
        else:
            logger.warning(
                f"Contact Us to email not found, so contact us email not sent"
            )
        return BaseResponseSchema(
            success=True, message="Contact Us created successfully"
        )

    async def get_contact_us(
        self, skip: int = 1, limit: int = 10
    ) -> ListContactUsResponseSchema:
        data = await self.repository.get_contact_us(skip, limit)
        return ListContactUsResponseSchema(
            data=data, success=True, message="Contact Us List retrieved successfully"
        )

    async def get_contact_us_by_id(
        self, contact_us_id: str
    ) -> DetailContactUsResponseSchema:
        data = await self.repository.get_contact_us_by_id(contact_us_id)
        if not data:
            raise HTTPException(status_code=404, detail="Contact Us not found")
        return DetailContactUsResponseSchema(
            data=data, success=True, message="Contact Us retrieved successfully"
        )
