from fastapi import APIRouter, Depends
from app.controllers.email_setting_controller import EmailSettingController
from app.schemas.email_settings_schema import EmailSettingsSchema
from app.services.common_service import CommonService
from app.schemas.user_schema import UserTokenDecodedData


router = APIRouter(prefix="/email-settings", tags=["Email Settings"])


@router.post("/create")
async def create_email_settings(
    email_settings: EmailSettingsSchema,
    controller: EmailSettingController = Depends(EmailSettingController),
    _token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    return await controller.create_email_settings(email_settings)


@router.get("/list")
async def get_email_settings(
    controller: EmailSettingController = Depends(EmailSettingController),
    _token: UserTokenDecodedData = Depends(CommonService.verify_token_get_user),
):
    return await controller.get_email_settings()
