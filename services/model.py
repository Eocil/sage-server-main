from models.user import User
from models.llm import LLMModel

from langchain_manager.models import llms

from exceptions.services import ServiceException, ServiceError

from enums.services_status import ServicesStatusEnum


class ModelService:

    def __init__(self, user: User) -> None:
        self.user = user
        self.chat_model: list[LLMModel] = []
        self.search_model: list[LLMModel] = []
        self.image_model: list[LLMModel] = []

        for llm in llms:
            if llm.is_chat_model:
                self.chat_model.append(llm)
            if llm.is_search_model:
                self.search_model.append(llm)
            if llm.is_image_model:
                self.image_model.append(llm)

    def __validate_models(self, llm: LLMModel) -> bool:
        """
        验证 LLM 是否允许该用户使用
        """
        try:
            if llm.has_permission(self.user.group):
                return True
            else:
                raise ServiceException(None, ServicesStatusEnum.MODEL_PERMISSION_DENIED)
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def get_chat_model(self, model_name: str) -> LLMModel:
        """
        获取聊天模型
        """
        try:
            for llm in self.chat_model:
                if llm.model_name == model_name:
                    if self.__validate_models(llm):
                        return llm
                    else:
                        raise ServiceException(
                            None, ServicesStatusEnum.GET_CHAT_MODEL_FAILED
                        )
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def get_search_model(self, model_name: str) -> LLMModel:
        """
        获取搜索模型
        """
        try:
            for llm in self.search_model:
                if llm.model_name == model_name:
                    if self.__validate_models(llm):
                        return llm
                    else:
                        raise ServiceException(
                            None, ServicesStatusEnum.GET_SEARCH_MODEL_FAILED
                        )
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def get_image_model(self, model_name: str) -> LLMModel:
        """
        获取图片模型
        """
        try:
            for llm in self.image_model:
                if llm.model_name == model_name:
                    if self.__validate_models(llm):
                        return llm
                    else:
                        raise ServiceException(
                            None, ServicesStatusEnum.GET_IMAGE_MODEL_FAILED
                        )
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def get_embedding_model(self, model_name: str) -> LLMModel:
        """
        获取嵌入模型
        """
        try:
            for llm in llms:
                if llm.model_name == model_name:
                    if self.__validate_models(llm):
                        return llm
                    else:
                        raise ServiceException(
                            None, ServicesStatusEnum.GET_EMBEDDING_MODEL_FAILED
                        )
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    async def get_available_models(self) -> list[LLMModel]:
        """
        获取用户可用的所有模型
        """
        available_models = []
        try:
            for llm in llms:
                if llm.has_permission(self.user.group):
                    available_models.append(llm.to_dict())
            return available_models
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    @staticmethod
    async def admin_get_model(model_name: str) -> LLMModel:
        """
        管理员获取模型
        """
        try:
            for llm in llms:
                if llm.model_name == model_name:
                    return llm
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)
