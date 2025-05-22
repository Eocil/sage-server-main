from fastapi import Request
from fastapi.responses import JSONResponse
from enums.message_enum import ServicesStatusEnum

from utils.result_vo import ResultVO

import traceback


class ServiceException(Exception):
    def __init__(self, exception: Exception, status_enum: ServicesStatusEnum):
        self.exception = exception
        self.status_enum = status_enum

class ServiceError(Exception):
    def __init__(self, exception: Exception, t: traceback = traceback):
        self.exception = exception
        self.traceback = t.format_exc()
    
    def __str__(self):
        return f"{self.exception}\n{self.traceback}"


class ServiceExceptionHandler:

    @staticmethod
    async def handle_exception(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except ServiceException as e:
            result = ResultVO(
                status=str(e.status_enum.code), message=e.status_enum.message, data=None
            )
            return JSONResponse(content=result.dict())
        
    @staticmethod
    async def handle_error(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except ServiceError as e:
            return 
