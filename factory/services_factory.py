from fastapi import Depends
import uuid

from services.token import AccessTokenService
from services.auth import AuthService
from services.user import UserService
from services.topic import TopicService
from services.chat import ChatService
from services.history import HistoryService
from services.model import ModelService
from services.stream import StreamService

from langchain_manager.llm_manager import LLMManager

from models.setting import Settings


def get_user_service(
    token_data: dict = Depends(AccessTokenService.get_token_data),
) -> UserService:
    """
    获取用户服务工厂函数
    """
    return UserService(token_data["uuid"])


async def get_auth_service(
    uuid: str = str(uuid.uuid4()),
) -> AuthService:
    """
    获取授权服务工厂函数
    """
    return AuthService(uuid)


async def get_topic_service(
    user_service: UserService = Depends(get_user_service),
) -> TopicService:
    """
    获取话题服务工厂函数
    """
    return TopicService(await user_service.get_user())


async def get_history_service(
    user_service: UserService = Depends(get_user_service),
) -> HistoryService:
    """
    获取话题详情服务工厂函数
    """
    return HistoryService(await user_service.get_user())


async def get_model_service(
    user_service: UserService = Depends(get_user_service),
) -> ModelService:
    """
    获取模型服务工厂函数
    """
    return ModelService(await user_service.get_user())


async def get_llm_manager(
    settings: Settings,
    topic_id: str = None,
    user_service: UserService = Depends(get_user_service),
    model_service: ModelService = Depends(get_model_service),
) -> LLMManager:
    return LLMManager(await user_service.get_user(), settings, topic_id, model_service)


async def get_chat_service(
    user_service: UserService = Depends(get_user_service),
    topic_service: TopicService = Depends(get_topic_service),
    history_service: HistoryService = Depends(get_history_service),
    llm_manager: LLMManager = Depends(get_llm_manager),
) -> ChatService:
    """
    获取聊天服务工厂函数
    """
    return ChatService(
        await user_service.get_user(),
        topic_service,
        history_service,
        llm_manager,
    )


async def get_stream_service() -> StreamService:
    """
    获取聊天服务工厂函数
    """
    return StreamService()
