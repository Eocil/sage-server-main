from fastapi import APIRouter, Depends

from services.token import AccessTokenService
from services.topic import TopicService
from services.history import HistoryService

from factory.services_factory import get_topic_service, get_history_service

from utils.result_vo import ResultVO

router = APIRouter()


@router.get("/topics", dependencies=[Depends(AccessTokenService.verify_access_token)])
async def get_topics(
    topic_service: TopicService = Depends(get_topic_service),
    offset: int = 0,
    limit: int = 20,
):
    """
    获取话题记录
    """
    _result = await topic_service.get_topics(offset, limit)
    return ResultVO(status="200", message="sucess", data=_result)


@router.delete("/topic", dependencies=[Depends(AccessTokenService.verify_access_token)])
async def delete_topic(
    topic_id: str,
    topic_service: TopicService = Depends(get_topic_service),
    history_service: HistoryService = Depends(get_history_service),
):
    """
    删除话题记录
    """
    await topic_service.validate_topic_id(topic_id)
    await topic_service.delete_topic(topic_id)
    await history_service.delete_history(topic_id)

    return ResultVO(status="200", message="sucess", data=None)
