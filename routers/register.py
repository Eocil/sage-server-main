from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from factory.services_factory import get_auth_service

from utils.result_vo import ResultVO

from services.auth import AuthService

from config.auth import RegisterConfig

router = APIRouter()


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    invite_code: Optional[str] = None


@router.get("/page/register")
async def registerPage():
    """
    返回用户注册页面的接口与服务器注册信息。
    """
    return ResultVO(status="200", message="success", data={"enable_invitation_code": RegisterConfig.ENABLE_INVITATION_CODE})


@router.post("/register")
async def register_post(
    request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)
):
    """
    处理用户注册请求的接口。
    """

    await auth_service.register(
        request.username, request.email, request.password, request.invite_code
    )
    return ResultVO(status="200", message="注册成功", data=None)
