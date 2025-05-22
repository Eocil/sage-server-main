from models.setting import Settings
from models.llm import LLMModel, LLMStatus

from langchain_manager.services.llm_chat import ChatLLM
from langchain_manager.services.llm_title import TitleLLM
from langchain_manager.services.agent_internet import InternetLLM
from langchain_manager.services.llm_sort import SortLLM
from langchain_manager.services.agent_python import PythonLLM

from services.model import ModelService
from models.user import User

from langchain_manager.utils.history import get_session_history

from exceptions.manager import ManagerException
from enums.manager_status import ManagersStatusEnum

import time
import asyncio

class LLMManager:

    def __init__(
        self, user: User, settings: Settings, topic_id: str, model_service: ModelService
    ) -> None:
        self.user = user
        self.settings = settings
        self.topic_id = topic_id
        self.model_service = model_service
        self.config = {"configurable": {"session_id": topic_id}}

    async def invoke(
        self,
        history_id: str,
        topic_id: str,
        history_list: dict,
        prompt: str,
        callback: any,
        file_ids: list[str] = None,
    ):
        """
        调用 LLM 生成回复。
        """
        try:
            _full_message = ""

            system_llm = await self.model_service.admin_get_model("GPT-4o")
            llm = await self.model_service.get_chat_model(
                self.settings.large_language_model
            )
            search_model = await self.model_service.get_search_model(
                self.settings.search_model
            )

            if self.settings.textual_context == "false":
                history_list = None

            get_session_history(
                self.topic_id,
                None if not history_list else history_list,
                False if history_list else True,
            )

            yield LLMStatus("topic_id", topic_id)
            yield LLMStatus("history_id", history_id)

            if llm is None or search_model is None:
                yield LLMStatus("error", "Model not available")
                return

            yield LLMStatus("status", 0)

            if file_ids:
                for file_id in file_ids:
                    yield LLMStatus("file_id", file_id)


            start_time = time.time()  # 记录开始时间

            if llm.function_call is False:
                scheduling = "@Chat"
            else:
                scheduling = await self.__invoke_sort(
                    prompt=prompt, llm=system_llm, hasFile=True if file_ids else False
                )
            end_time = time.time()  # 记录结束时间
            elapsed_time = end_time - start_time  # 计算用时
            print(
                f"Elapsed time for scheduling: {elapsed_time:.2f} seconds"
            )  # 打印用时

            print(f"scheduling: {scheduling}")

            if scheduling == "@Chat":
                _iterator = await self.__invoke_chat(prompt=prompt, llm=llm)

            elif scheduling == "@Internet":
                _iterator = await self.__invoke_internet(
                    prompt=prompt, llm=llm, search_model=search_model
                )

            elif scheduling == "@Python":
                _iterator = await self.__invoke_python(
                    prompt=prompt, config=self.config, llm=llm
                )

            else:
                _iterator = await self.__invoke_chat(prompt=prompt, llm=llm)

            async for response in _iterator:
                if response.type == "answer":
                    _full_message += response.chunk
                yield response

            yield LLMStatus("status", 1)

            _title = await self.__invoke_title(
                prompt=prompt, answer=_full_message, llm=system_llm
            )

            if callback:
                yield LLMStatus("title", _title)
                await callback(self.topic_id, _title)

            yield LLMStatus("status", 2)
        except Exception as e:
            yield LLMStatus("error", "Model invoke error")
            raise ManagerException(e, ManagersStatusEnum.INVOKE_LLM_FAILED)

    async def __invoke_sort(self, prompt: str, llm: LLMModel, hasFile: bool = False):
        """
        调用Sort模型调度LLM。
        """
        try:
            return await SortLLM.invoke(prompt=prompt, config=self.config, llm=llm, hasFile=hasFile)
        except Exception as e:
            raise ManagerException(e, ManagersStatusEnum.INVOKE_SORT_FAILED)

    async def __invoke_chat(self, prompt: str, llm: LLMModel):
        """
        调用Chat模型生成回复。
        """
        try:
            return ChatLLM.invoke(prompt=prompt, config=self.config, llm=llm)
        except Exception as e:
            raise ManagerException(e, ManagersStatusEnum.INVOKE_CHAT_FAILED)

    async def __invoke_internet(
        self, prompt: str, llm: LLMModel, search_model: LLMModel
    ):
        """
        调用Internet模型生成回复。
        """
        try:
            return InternetLLM.invoke(
                prompt=prompt, config=self.config, llm=llm, search_model=search_model
            )
        except Exception as e:
            raise ManagerException(e, ManagersStatusEnum.INVOKE_INTERNET_FAILED)

    async def __invoke_python(self, prompt: str, config: dict, llm: LLMModel):
        """
        调用Python模型生成回复。
        """
        try:
            return PythonLLM.python_run(prompt=prompt, config=config, llm=llm)
        except Exception as e:
            raise ManagerException(e, ManagersStatusEnum.INVOKE_PYTHON_FAILED)

    async def __invoke_title(self, prompt: str, answer: str, llm: LLMModel) -> str:
        """
        调用Title模型的方法。
        """
        try:
            return await TitleLLM.invoke(prompt=prompt, answer=answer, llm=llm)
        except Exception as e:
            raise ManagerException(e, ManagersStatusEnum.INVOKE_TITLE_FAILED)

    def get_settings(self) -> Settings:
        """
        获取设置。
        """
        return self.settings

    def set_topic_id(self, topic_id: str):
        """
        设置话题ID。
        """
        self.topic_id = topic_id
        self.config = {"configurable": {"session_id": topic_id}}
