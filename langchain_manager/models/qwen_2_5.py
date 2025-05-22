from langchain_community.chat_models.tongyi import ChatTongyi
from models.llm import LLMModel
import os

model_name = os.environ.get("TONGYI_MODEL_NAME", "Qwen-7B")
api_key = os.environ.get("TONGYI_API_KEY", "")


def init() -> LLMModel:
    model = ChatTongyi(
        model=model_name,
        api_key=api_key,
    )
    return LLMModel(
        model_name="Tongyi-Qwen",
        model=model,
        type="chat",
        allowed_group=["default"],
        description="",
        version="1.0.0",
    )
