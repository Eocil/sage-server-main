from models.user import User

from enums.services_status import ServicesStatusEnum

from exceptions.services import ServiceException, ServiceError

from repositories.topic import TopicRepository


import datetime
import uuid


class TopicService:

    def __init__(self, user: User) -> None:
        self.user = user
        self.repo = TopicRepository(user.uuid)

    async def update_title(self, topic_id: str, title: str) -> bool:
        """
        更新话题标题
        """
        try:
            await self.repo.update_title(topic_id, title)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def create_topic(self, title: str = None) -> str:
        """
        创建话题记录
        """
        _topic_id = str(uuid.uuid4())
        _title = title if title else None
        _time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            await self.repo.create(_topic_id, _title, _time)
            return _topic_id
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def get_topic(self, topic_id: str) -> dict:
        """
        获取话题记录
        """
        try:
            _result = await self.repo.read(topic_id)
            if _result:
                return _result
            else:
                raise ServiceException(None, ServicesStatusEnum.TOPIC_NOT_FOUND)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def get_topics(self, offset: int, limit: int) -> dict:
        """
        获取话题记录
        """
        try:
            return await self.repo.read_all(offset, limit)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def delete_topic(self, topic_id: str) -> bool:
        """
        删除话题记录
        """
        try:
            await self.get_topic(topic_id)
            await self.repo.delete(topic_id)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    @staticmethod
    async def validate_topic_id(topic_id: str) -> bool:
        """
        校验是否是uuid4
        """
        try:
            # 检查长度
            if len(topic_id) != 36:
                return False

            # 检查格式
            if not all(topic_id[i] == "-" for i in [8, 13, 18, 23]):
                return False

            # 尝试解析
            try:
                val = uuid.UUID(topic_id, version=4)
            except ValueError:
                return False

            # 检查是否是UUID4
            if str(val) == topic_id:
                return True
            else:
                ServiceException(None, ServicesStatusEnum.INVALID_TOPIC_ID)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)
