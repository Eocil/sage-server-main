from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.auth import AuthService

from factory.services_factory import get_auth_service

from utils.result_vo import ResultVO


router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


@router.get("/page/login")
async def loginPage():
    """
    返回用户登录页面的接口。
    """
    return {}


@router.post("/login")
async def login_post(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    处理用户登录请求的接口。
    """

    _redirect_url = None

    token = await auth_service.login(request.email, request.password)

    

    if token:
        _redirect_url = "/page/chat"

        return ResultVO(
            status="200",
            message="sucess",
            data={"token": token, "redirect_url": _redirect_url},
        )
