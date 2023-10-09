from fastapi import FastAPI

from app.routers.tasks import task_router
from app.routers.users import user_router
from app.routers.admin import admin_router


app=FastAPI(
    title="To Do List app",
    description="Manages the list of to do tasks",
    version="0.0.1",
    openapi_url="/https://todolist//openapi.json"
)

app.include_router(admin_router)
app.include_router(task_router)
app.include_router(user_router)