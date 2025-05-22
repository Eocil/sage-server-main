from fastapi import APIRouter, Depends

from services.token import AccessTokenService
from services.history import HistoryService
from services.topic import TopicService

from factory.services_factory import get_history_service, get_topic_service

from utils.result_vo import ResultVO

router = APIRouter()


@router.get("/history", dependencies=[Depends(AccessTokenService.verify_access_token)])
async def get_history(
    topic_id: str,
    history_service: HistoryService = Depends(get_history_service),
    topic_service: TopicService = Depends(get_topic_service),
):
    """
    获取话题详情
    """
    # 校验是否是uuid4
    await topic_service.validate_topic_id(topic_id=topic_id)
    _result = await history_service.get_history(topic_id=topic_id)

    return ResultVO(status="200", message="sucess", data=_result)
