from fastapi import APIRouter, Depends

from services.token import AccessTokenService

from services.user import UserService

from factory.services_factory import get_user_service

from utils.result_vo import ResultVO

router = APIRouter()


@router.get("/user", dependencies=[Depends(AccessTokenService.verify_access_token)])
async def get_models(
    user_service: UserService = Depends(get_user_service)
):
    """
    用户信息的接口。
    """
    _result = await user_service.get_user()
    _result_dict = _result.__dict__
    _result_dict["hashed_password"] = "******"
    return ResultVO(status="200", message="sucess", data=_result_dict)
