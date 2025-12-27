from app.services.portfolio_service import PortfolioService
from app.schemas.portfolio_schema import ContactUsSchema

class PortfolioController:
    def __init__(self):
        self.portfolio_service = PortfolioService()
    
    async def create_contact_us(self, contact_us: ContactUsSchema):
        return await self.portfolio_service.create_contact_us(contact_us)
    
    async def get_contact_us(self, skip: int = 1, limit: int = 10):
        return await self.portfolio_service.get_contact_us(skip, limit)
    
    async def get_contact_us_by_id(self, contact_us_id: str):
        return await self.portfolio_service.get_contact_us_by_id(contact_us_id)