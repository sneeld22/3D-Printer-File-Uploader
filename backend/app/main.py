from fastapi import FastAPI
from app.api.v1 import api_router

app = FastAPI(title="3D Print Portal", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")
