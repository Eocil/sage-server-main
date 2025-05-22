
from pydantic import BaseModel

class Settings(BaseModel):
    """
    用于存储Chat接口的设置模型
    """

    textual_context: str
    large_language_model: str
    image_model: str
    search_model: str
    retrieval_tag: str