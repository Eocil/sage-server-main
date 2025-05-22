from langchain_openai import ChatOpenAI
from models.llm import LLMModel
import os

api_key = os.environ.get("DEEPSEEK_API_KEY", "")
base_url = os.environ.get("DEEPSEEK_API_URL", "")
api_version = os.environ.get("DEEPSEEK_API_VERSION", "V3")

def init() -> LLMModel:
    
    llm = ChatOpenAI(
        api_key=api_key,
        base_url=base_url,
        model="deepseek-chat",
    )

    return LLMModel(
        model_name="DeepSeek-V3",
        model=llm,
        type="chat",
        allowed_group=["default"],
        description="",
        version=api_version,
    )
