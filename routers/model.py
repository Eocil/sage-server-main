from fastapi import APIRouter, Depends

from services.token import AccessTokenService

from services.model import ModelService

from factory.services_factory import get_model_service

from utils.result_vo import ResultVO

router = APIRouter()


@router.get("/models", dependencies=[Depends(AccessTokenService.verify_access_token)])
async def get_models(
    model_service: ModelService = Depends(get_model_service),
):
    """
    用户发送消息的接口。
    """
    _result = await model_service.get_available_models()
    return ResultVO(status="200", message="sucess", data=_result)
