import base64
from fastapi.responses import Response
import json

class MultipleImagesResponse(Response):
    def __init__(self, images: list[bytes], *args, **kwargs):
        # 将图片内容转换为 Base64 编码
        content = json.dumps({"images": [base64.b64encode(img).decode('utf-8') for img in images]})
        super().__init__(content=content, media_type="application/json", *args, **kwargs)