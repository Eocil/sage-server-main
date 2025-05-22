from services.history import HistoryService

from exceptions.services import ServiceException, ServiceError

from fastapi.responses import StreamingResponse, FileResponse
from fastapi import UploadFile

from enums.services_status import ServicesStatusEnum

from models.user import User

from langchain_manager.utils.loader import Loaders
from milvus.curd import MilvusCURD

import json
import os
import uuid
import hashlib
import datetime
import aiofiles
from urllib.parse import quote

from config.model import PYTHON_SAVE_DIR, IMAGE_SAVE_DIR, FILE_SAVE_DIR

from repositories.file import FileRepository
from utils.mult_response import MultipleImagesResponse


class FileService:

    pyhton_path = PYTHON_SAVE_DIR
    image_path = IMAGE_SAVE_DIR
    file_path = FILE_SAVE_DIR

    def __init__(self, user: User, history_service: HistoryService) -> None:
        self.user = user
        self.history_service = history_service
        self.repo = FileRepository(user.uuid)


    async def get_code(self, topic_id: str, code_id: str, type: str):
        """
        获取代码
        """
        try:
            _history_list = await self.history_service.get_history(topic_id)

            for _history in _history_list:
                data = json.loads(_history["extra_data"])
                if "python" in data and data["python"]:
                    if code_id == data["python"][0]["code_id"]:

                        _suffix_map = {"code": ".py", "output": ".txt", "image": ".jpg"}
                        if type in _suffix_map:

                            _suffix = _suffix_map[type]
                            if type == "image":
                                # 查找所有匹配的图片文件
                                image_files = []
                                base_path = FileService.image_path
                                
                                # 遍历目录查找所有匹配的图片
                                if os.path.exists(base_path):
                                    for file_name in os.listdir(base_path):
                                        if file_name.startswith(code_id + "_") and file_name.endswith(_suffix):
                                            file_path = os.path.join(base_path, file_name)
                                            # 读取图片内容为 bytes
                                            with open(file_path, "rb") as f:
                                                image_files.append(f.read())
                            
                                if image_files:
                                    # 使用自定义响应类返回图片内容列表
                                    return MultipleImagesResponse(image_files)

                                media_type = "image/jpeg"
                            else:
                                file_path = os.path.join(
                                    FileService.pyhton_path, code_id + _suffix
                                )
                                media_type = (
                                    "text/plain"
                                    if _suffix in [".py", ".txt"]
                                    else "application/octet-stream"
                                )

                            if os.path.exists(file_path):
                                return FileResponse(file_path, media_type=media_type)

            raise ServiceException(None, ServicesStatusEnum.CODE_NOT_FOUND)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

