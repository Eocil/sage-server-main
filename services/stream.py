import asyncio
from typing import AsyncIterator

from models.llm import LLMMessage, LLMStatus

from exceptions.services import ServiceException, ServiceError

from fastapi.responses import StreamingResponse


class StreamService:

    @staticmethod
    async def stream(
        message: AsyncIterator[LLMMessage | LLMStatus],
    ) -> StreamingResponse:
        """
        流式输出
        """
        try:
            return StreamingResponse(
                StreamService.event_generator(message), media_type="text/event-stream"
            )
        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)

    @staticmethod
    async def event_generator(
        message: AsyncIterator[LLMMessage | LLMStatus],
    ) -> AsyncIterator[LLMMessage | LLMStatus]:
        """
        一个生成器函数，用于持续生成SSE事件。
        """
        try:
            async for obj in message:
                model: LLMMessage | LLMStatus = obj

                if isinstance(model, LLMStatus):
                    _type = model.type
                    _chunk = model.message
                    yield f"event: {_type}\ndata: {_chunk}\n\n"
                else:
                    _type = model.type
                    _chunk = model.chunk.encode("unicode-escape").decode("ascii")
                    yield f"event: {_type}\ndata: {_chunk}\n\n"

        except ServiceException as e:
            raise ServiceException(e, e.status_enum)
        except Exception as e:
            raise ServiceError(e)
