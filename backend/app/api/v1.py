from fastapi import APIRouter
from app.api.routes import files, auth

api_router = APIRouter()

api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])