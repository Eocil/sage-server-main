from passlib.context import CryptContext

from services.invite_code import InviteCodeService
from services.token import AccessTokenService
from services.user import UserService

from enums.services_status import ServicesStatusEnum

from exceptions.services import ServiceException, ServiceError

from config.auth  import RegisterConfig


class AuthService:

    def __init__(self, uuid: str) -> None:

        self.token_service = AccessTokenService()
        self.invite_code_service = InviteCodeService(uuid)
        self.user_service = UserService(uuid)

    async def login(self, email: str, password: str) -> str:
        """
        使用邮箱和密码登录
        """
        try:
            user = await UserService.get_user_by_email(email)
            if CryptContext(schemes=["bcrypt"], deprecated="auto").verify(
                password, user.hashed_password
            ):
                await self.token_service.create_access_token(user)

                return await self.token_service.get_access_token(user.uuid)

            else:
                raise ServiceException(None, ServicesStatusEnum.INVALID_PASSWORD)

        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def register(
        self, username: str, email: str, password: str, invite_code: str
    ) -> ServicesStatusEnum:
        """
        注册新用户
        """
        try:
            _invite_code_service = self.invite_code_service
            _user_service = self.user_service

            await _invite_code_service.check_invite_code(invite_code) if RegisterConfig.ENABLE_INVITATION_CODE else None
            await _user_service.check_email(email)

            await _invite_code_service.create_invite_code()
            await _user_service.create_user(
                username,
                email,
                password,
            )

        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)
