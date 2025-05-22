import os
from langchain_openai import AzureChatOpenAI
from langchain_core.runnables import ConfigurableField
from models.llm import LLMModel

api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "")
azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
azure_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")


def init() -> LLMModel:
    
    llm = AzureChatOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint,
        azure_deployment=azure_deployment,
        temperature=0,
    )


    return LLMModel(
        model_name="GPT-4o",
        model=llm,
        type="chat",
        allowed_group=["default"],
        description="",
        version=api_version,
    )
