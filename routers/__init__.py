import os
import importlib

from main import app

"""
#Template to add a new route

from fastapi import APIRouter

router = APIRouter()
"""

def init_routers():
    routers = []
    print("[Server] Initializing")
    for file in os.listdir(os.path.dirname(__file__)):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"routers.{file[:-3]}"
            module = importlib.import_module(module_name)
            router = getattr(module, "router", None)
            if router:
                print(f"[Server]  - {module_name}")
                routers.append(router)
    for route in routers:
        app.include_router(route)