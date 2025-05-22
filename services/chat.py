import json
from models.user import User

from services.topic import TopicService
from services.history import HistoryService

from langchain_manager.llm_manager import LLMManager

from exceptions.services import ServiceException, ServiceError

class ChatService:
    def __init__(
        self,
        user: User,
        topic_service: TopicService,
        history_service: HistoryService,
        llm_manager: LLMManager,
    ) -> None:
        self.user = user
        self.topic_service = topic_service
        self.history_service = history_service
        self.llm_manager = llm_manager

    async def invoke(self, topic_id: str, prompt: str, file_ids: list[str] = None):
        """
        用户发送消息业务逻辑。
        负责记录llm输出的消息，保存对话记录。
        """
        try:
            if not topic_id:
                _topic_id = await self.topic_service.create_topic(title=None)
                self.llm_manager.set_topic_id(topic_id=_topic_id)
            else:
                _topic_id = topic_id

            _history_list = await self.history_service.get_history(topic_id=_topic_id)
            _topic = await self.topic_service.get_topic(topic_id=_topic_id)

            _history_id = await self.history_service.create_history(
                prompt=prompt,
                topic_id=_topic_id,
                answer=None,
                model=self.llm_manager.get_settings().large_language_model,
                file_ids=file_ids,
                extra_data=None,
            )

            print(f"topic_id: {_topic_id}, history_id: {_history_id}")

            _full_message = ""
            _extra_data = {}
            _iterator = self.llm_manager.invoke(
                history_id=_history_id,
                topic_id=_topic_id,
                history_list=_history_list,
                prompt=prompt,
                file_ids=file_ids,
                callback=self.title_callback if not _topic["title"] or _topic["title"] == "未命名标题" else None,
            )

            async for response in _iterator:
                if response.type == "answer":
                    _full_message += response.chunk

                elif response.type in ("image", "internet", "python"):
                    key = response.type
                    if key not in _extra_data:
                        _extra_data[key] = []

                    if key == "internet":
                        data = json.loads(response.message)
                    elif key == "python":
                        data = {"code_id": response.message}
                    else:  # image
                        data = {"image_id": response.message}

                    _extra_data[key].append(data)
                    await self.history_service.update_extra_data(
                        topic_id=_topic_id, history_id=_history_id, extra_data=_extra_data
                    )

                yield response
            await self.history_service.update_answer(
                topic_id=_topic_id, history_id=_history_id, answer=_full_message
            )

        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def title_callback(self, topic_id: str, title: str):
        """
        更新对话标题的回调函数。
        """
        try:
            await self.topic_service.update_title(topic_id=topic_id, title=title)
            return title
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)
