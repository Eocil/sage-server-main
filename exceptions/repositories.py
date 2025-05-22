from fastapi import Request


class RepositoryError(Exception):
    def __init__(self, exception: Exception, sql: str, params: tuple) -> None:
        self.exception = exception
        self.sql = sql
        self.params = params
        super().__init__(self.exception, self.sql, self.params)


class RepositoriesErrorHandler:

    @staticmethod
    async def handle_error(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except RepositoryError as e:
            print(e.exception)
            print(e.sql)
            print(e.params)
            
