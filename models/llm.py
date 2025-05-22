from langchain_core.runnables import RunnableSerializable
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import AzureChatOpenAI
from langchain_community.chat_models.tongyi import ChatTongyi


class LLMModel:

    model_name: str
    model: RunnableSerializable | AzureChatOpenAI | ChatTongyi | TavilySearchResults
    type: str

    allowed_group: list[str]
    description: str
    version: str

    """
    Optional:

    url_keyword: search model's return url dict keyword
    content_keyword: search model's return web content dict keyword
    """
    results_path: str = ""
    url_keyword: str = ""
    title_keyword: str = ""
    content_keyword: str = ""
    # Resoning model not support function call
    function_call: bool = True

    def __init__(
        self,
        model_name,
        model,
        type,
        allowed_group,
        description,
        version,
        results_path="",
        url_keyword="",
        title_keyword="",
        content_keyword="",
        function_call=True,
    ):
        self.model_name = model_name
        self.model = model
        self.type = type
        self.allowed_group = allowed_group
        self.description = description
        self.version = version

        self.results_path = results_path
        self.url_keyword = url_keyword
        self.title_keyword = title_keyword
        self.content_keyword = content_keyword
        self.function_call = function_call

    def to_dict(self):
        return {
            "model_name": self.model_name,
            "type": self.type,
            "description": self.description,
            "version": self.version,
            "results_path": self.results_path,
            "url_keyword": self.url_keyword,
            "title_keyword": self.title_keyword,
            "content_keyword": self.content_keyword,
            "function_call": self.function_call,
        }

    def is_chat_model(self) -> bool:
        return self.type == "chat"

    def is_search_model(self) -> bool:
        return self.type == "search"

    def is_image_model(self) -> bool:
        return self.type == "image"

    def has_permission(self, user_group: str) -> bool:
        if user_group == "admin":
            return True
        return user_group in self.allowed_group


class LLMMessage:

    type: str
    chunk: str

    def __init__(self, type, chunk):
        self.type = type
        self.chunk = chunk


class LLMStatus:

    type: str
    message: str

    def __init__(self, type, message):
        self.type = type
        self.message = message
