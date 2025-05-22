from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from models.llm import LLMModel
from config.model import SERACH_LLM_RETURN_COUNT

tavily_api_key = "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"


def init() -> LLMModel:
    model = TavilySearchResults(
        max_results=SERACH_LLM_RETURN_COUNT,
        search_depth="advanced",
        include_answer=True,
        api_wrapper=TavilySearchAPIWrapper(
            tavily_api_key=tavily_api_key,
        ),
    )
    return LLMModel(
        model_name="Tavily",
        model=model,
        type="search",
        allowed_group=["default"],
        description="",
        version="1.0.0",
        results_path="results",
        url_keyword="url",
        title_keyword="title",
        content_keyword="content",
    )
