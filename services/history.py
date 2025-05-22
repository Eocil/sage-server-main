from models.user import User

from exceptions.services import ServiceException, ServiceError

from enums.services_status import ServicesStatusEnum

from repositories.history import HistoryRepository

import uuid
import datetime
import json


class HistoryService:

    def __init__(self, user: User) -> None:
        self.user = user
        self.repo = HistoryRepository(user.uuid)

    async def get_history(self, topic_id: str) -> dict:
        """
        获取话题详情
        """
        try:
            return await self.repo.read(topic_id=topic_id)

        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def create_history(
        self,
        topic_id: str,
        prompt: str,
        answer: str,
        model: str,
        file_ids: list[str],
        extra_data: str,
    ) -> dict:
        """
        创建话题详情
        """
        _history_id = str(uuid.uuid4())
        _time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            await self.repo.create(
                topic_id=topic_id,
                history_id=_history_id,
                time=_time,
                prompt=prompt,
                model=model,
                file_ids=str(file_ids) if file_ids else None,
                extra_data=json.dumps(extra_data) if extra_data else "{}",
                answer=answer,
            )
            return _history_id
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def update_answer(self, topic_id: str, history_id: str, answer: str) -> bool:
        """
        更新话题answer
        """
        try:
            await self.repo.update_answer(
                topic_id=topic_id, history_id=history_id, answer=answer
            )
            return
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def update_extra_data(
        self, topic_id: str, history_id: str, extra_data: str
    ) -> bool:
        """
        更新话题extra_data
        """
        try:

            await self.repo.update_extra_data(
                topic_id=topic_id,
                history_id=history_id,
                extra_data=json.dumps(extra_data),
            )
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def delete_history(self, topic_id: str):
        """
        删除话题记录
        """
        try:
            await self.repo.delete(topic_id)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)
