from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from services.token import AccessTokenService
from services.topic import TopicService
from services.file import FileService

from fastapi import UploadFile, File

from factory.services_factory import get_topic_service, get_file_service

from utils.result_vo import ResultVO


router = APIRouter()


@router.get(
    "/file/code", dependencies=[Depends(AccessTokenService.verify_access_token)]
)
async def get_code(
    topic_id: str,
    code_id: str,
    type: str,
    topic_service: TopicService = Depends(get_topic_service),
    file_service: FileService = Depends(get_file_service),
):
    """
    获取code
    """
    # 校验是否是uuid4
    await topic_service.validate_topic_id(topic_id=topic_id)

    return await file_service.get_code(topic_id=topic_id, code_id=code_id, type=type)

@router.get(
    "/file/download", dependencies=[Depends(AccessTokenService.verify_access_token)]
)
async def download_file(
    file_id: str,
    file_service: FileService = Depends(get_file_service),
):
    """
    下载文件
    """
    return await file_service.download_file(file_id=file_id)
