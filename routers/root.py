
from fastapi import APIRouter

from fastapi.responses import RedirectResponse
from fastapi.requests import Request


router = APIRouter()

# Purpose: Contains the router for the root path of the application.
@router.get("/")
async def router_root(request: Request):
    return RedirectResponse(url="/page/login", status_code=303)