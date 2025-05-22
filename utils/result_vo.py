from pydantic import BaseModel, Field
from typing import Optional



class ResultVO(BaseModel):
    status: str = Field(..., description="结果状态")
    message: Optional[str] = Field(None, description="结果消息")
    data: Optional[dict] = Field(None, description="结果数据")

    def __init__(self, status: str, message: Optional[str] = None, data: Optional[dict | list] = None):
        _data_dict = {}
        #把list类型转换成dict类型
        if not data:
            data = {}
        if isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, dict):
                    _data_dict[index] = item
        else:
            _data_dict = data
        super().__init__(status=status, message=message, data=_data_dict)

