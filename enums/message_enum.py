from enum import Enum

class ServicesStatusEnum(Enum):
    code: str
    message: str
    
    def __init__(self, code, message):
        self.code = code
        self.message = message