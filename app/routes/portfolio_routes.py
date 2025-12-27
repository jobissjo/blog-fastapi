from fastapi import APIRouter, Depends
from app.schemas.portfolio_schema import ContactUsSchema
from app.controllers.portfolio_controller import PortfolioController
from app.services.common_service import CommonService
from app.schemas.user_schema import UserTokenDecodedData

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/")
async def wake_up():
    return {"message": "Portfolio is running"}


@router.post("/contact-us")
async def contact_us(
    data: ContactUsSchema,
    controller: PortfolioController = Depends(PortfolioController),
):
    return await controller.create_contact_us(data)

@router.get("/contact-us")
async def get_contact_us(
    controller: PortfolioController = Depends(PortfolioController),
    skip: int = 1,
    limit: int = 10,
    _token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),

):
    return await controller.get_contact_us(skip, limit)

@router.get("/contact-us/{contact_us_id}")
async def get_contact_us_by_id(
    contact_us_id: str,
    controller: PortfolioController = Depends(PortfolioController),
    _token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    return await controller.get_contact_us_by_id(contact_us_id)
