from fastapi import APIRouter
from .health.routers import health
from .users.routers import users

api = APIRouter()
api.include_router(health, prefix="/health", tags=["health"])
api.include_router(users, prefix="/users", tags=["users"])
