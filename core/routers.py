from fastapi import APIRouter
from .health.routers import health
from .users.routers import users
from .store.routers import store

api = APIRouter()
api.include_router(health, prefix="/health", tags=["health"])
api.include_router(users, prefix="/users", tags=["users"])
api.include_router(store, prefix="/store", tags=["store"])
