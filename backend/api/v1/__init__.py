from fastapi import APIRouter
from .routers import auth_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
