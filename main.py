from fastapi import FastAPI
from fastapi.requests import Request

from exceptions.services import ServiceExceptionHandler
from exceptions.manager import ManagerExceptionHandler
from fastapi.middleware.cors import CORSMiddleware
from config import server

import os

app = FastAPI()


@app.middleware("http")
async def services_error_handler(request: Request, call_next):
    return await ServiceExceptionHandler.handle_exception(request, call_next)


@app.middleware("http")
async def managers_error_handler(request: Request, call_next):
    return await ManagerExceptionHandler.handle_exception(request, call_next)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():

    from routers import init_routers

    init_routers()


@app.on_event("shutdown")
async def shutdown():
    from repositories import close_pool

    await close_pool()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=server.HOST,
        port=server.PORT,
        reload=True,
    )
