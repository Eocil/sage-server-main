from repositories.user import UserRepository

from models.user import User

from passlib.context import CryptContext

from enums.services_status import ServicesStatusEnum

from exceptions.services import ServiceException, ServiceError


class UserService:

    def __init__(self, uuid: str) -> None:
        self.uuid = uuid
        self.repo = UserRepository(uuid)

    async def create_user(self, username: str, email: str, password: str) -> bool:
        """
        创建新用户
        """
        _uuid = self.uuid
        _group = "default"
        try:
            _hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash(
                password
            )
            await self.repo.create(username, email, _hashed_password, _group)
            return User(
                uuid=_uuid,
                username=username,
                email=email,
                hashed_password=_hashed_password,
                group=_group,
            )
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def get_user(self) -> User:
        """
        获取用户信息
        """
        try:
            _result = await self.repo.read()
            if _result:
                return User(
                    uuid=_result["uuid"],
                    username=_result["username"],
                    email=_result["email"],
                    hashed_password=_result["hashed_password"],
                    group=_result["group"],
                )
            else:
                raise ServiceException(None, ServicesStatusEnum.USER_NOT_FOUND)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    @staticmethod
    async def check_email(email: str) -> bool:
        """
        检查邮箱是否已经注册
        """
        try:
            if await UserRepository.check_email(email):
                raise ServiceException(None, ServicesStatusEnum.EMAIL_EXIST)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    @staticmethod
    async def get_user_by_email(email: str) -> User:
        """
        通过邮箱获取用户信息
        """
        try:
            _result = await UserRepository.read_by_email(email)
            if _result:
                return User(
                    uuid=_result["uuid"],
                    username=_result["username"],
                    email=_result["email"],
                    hashed_password=_result["hashed_password"],
                    group=_result["group"],
                )
            else:
                raise ServiceException(None, ServicesStatusEnum.USER_NOT_FOUND)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)
