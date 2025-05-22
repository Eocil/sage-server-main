from config.auth import AuthConfig

from models.user import User

import jwt
from datetime import datetime, timedelta
from fastapi import Request, HTTPException

from enums.services_status import ServicesStatusEnum

from exceptions.services import ServiceException, ServiceError

from repositories.token import TokenRepository


class AccessTokenService:

    def __init__(self):
        self.SECRET_KEY = AuthConfig.SECRET_KEY
        self.EXPIRE_TIME = AuthConfig.EXPIRE_TIME
        self.token_repository = TokenRepository()

    async def create_access_token(self, user: User) -> str:
        """
        创建访问令牌
        """
        try:
            _expire_time = timedelta(hours=self.EXPIRE_TIME)
            _token_data = {
                "uuid": user.uuid,
                "username": user.username,
                "email": user.email,
                "group": user.group,
                "exp": datetime.utcnow() + _expire_time,
            }
            _token = jwt.encode(_token_data, self.SECRET_KEY, algorithm="HS256")

            if await self.token_repository.read(user.uuid):
                await self.token_repository.update(user.uuid, _token)
            else:
                await self.token_repository.create(user.uuid, _token)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def get_access_token(self, uuid: str) -> str:
        """
        获取访问令牌
        """
        try:

            _token = await self.token_repository.read(uuid)
            return _token["token"]

        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    @staticmethod
    async def verify_access_token(request: Request):
        """
        验证访问令牌
        """
        try:
            token = request.headers.get("Authorization")
            status = await TokenRepository.check(token)

            if not status:
                raise ServiceException(None, ServicesStatusEnum.INVALID_ACCESS_TOKEN)

        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    @staticmethod
    async def decode_access_token(access_token: str):
        """
        解码访问令牌
        """
        try:
            try:
                return jwt.decode(
                    access_token, AuthConfig.SECRET_KEY, algorithms=["HS256"]
                )
            except Exception as e:
                raise ServiceException(e, ServicesStatusEnum.INVALID_ACCESS_TOKEN)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    @staticmethod
    async def get_token_data(request: Request) -> User:
        """
        获取令牌数据
        """
        try:
            try:
                access_token = request.headers.get("Authorization")
                return jwt.decode(
                    access_token, AuthConfig.SECRET_KEY, algorithms=["HS256"]
                )
            except Exception as e:
                raise ServiceException(e, ServicesStatusEnum.INVALID_ACCESS_TOKEN)

        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)
