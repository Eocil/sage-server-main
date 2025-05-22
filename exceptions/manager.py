from fastapi import Request

from enums.manager_status import ManagersStatusEnum


class ManagerException(Exception):
    def __init__(self, exception: Exception, status_enum: ManagersStatusEnum) -> None:
        self.exception = exception
        self.status_enum = status_enum


class ManagerExceptionHandler:

    @staticmethod
    async def handle_exception(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except ManagerException as e:
            print(" --",e.status_enum.code)
            print(" --",e.status_enum.message)
            
