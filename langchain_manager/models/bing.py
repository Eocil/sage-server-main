from langchain_community.utilities import BingSearchAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults
from models.llm import LLMModel
from config.model import SERACH_LLM_RETURN_COUNT
import os

bing_subscription_key = os.environ.get("BING_SUBSCRIPTION_KEY", "")


def init() -> LLMModel:
    model = BingSearchResults(
        api_wrapper=BingSearchAPIWrapper(
            bing_subscription_key=bing_subscription_key,
            bing_search_url="https://api.bing.microsoft.com/v7.0/search",
            k=SERACH_LLM_RETURN_COUNT,
        ),
    )
    return LLMModel(
        model_name="Bing",
        model=model,
        type="search",
        allowed_group=["default"],
        description="",
        version="1.0.0",
        results_path=None,
        url_keyword="link",
        title_keyword="title",
        content_keyword="snippet",
    )
