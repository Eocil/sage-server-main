from fastapi import APIRouter, Depends, Query

from utils.result_vo import ResultVO

from pydantic import BaseModel

from services.token import AccessTokenService
from services.chat import ChatService
from services.topic import TopicService
from services.stream import StreamService

from models.setting import Settings

from factory.services_factory import (
    get_chat_service,
    get_topic_service,
    get_stream_service,
)

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str


@router.get(
    "/page/chat", dependencies=[Depends(AccessTokenService.verify_access_token)]
)
async def loginPage():
    """
    返回用户Chat页面的接口。
    """
    return ResultVO(status="200", message="sucess", data=None)


@router.post("/chat", dependencies=[Depends(AccessTokenService.verify_access_token)])
async def post_chat(
    settings: Settings,
    request: ChatRequest,
    topic_id: str = None,
    file_id: list[str] = Query(None),
    chat_service: ChatService = Depends(get_chat_service),
    topic_service: TopicService = Depends(get_topic_service),
    stream_service: StreamService = Depends(get_stream_service),
):
    """
    用户发送消息的接口。
    """
    if topic_id:
        await topic_service.validate_topic_id(topic_id=topic_id)

    if file_id:
        if len(file_id) > 3:
            return "File is greater than 3"

    chat_response = chat_service.invoke(
        topic_id=topic_id, prompt=request.prompt, file_ids=file_id
    )
    return await stream_service.stream(chat_response)
