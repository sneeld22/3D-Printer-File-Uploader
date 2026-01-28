from app.core.logging import setup_logging
setup_logging()  # MUST BE FIRST

from fastapi import FastAPI
#from app.api.v1 import api_router

from app.api.v1 import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.db.models import User, UserRole, RoleEnum
from app.core.config import settings
from app.utils.bootstrap import bootstrap_roles
import uuid

def add_users():
    db = SessionLocal()
    try:
        bootstrap_roles(db)
    finally:
        db.close()

# Create database tables
Base.metadata.create_all(bind=engine)
add_users()

app = FastAPI(title="3D Print Portal", version="1.0.0")

# Add CORS middleware
origins = [
    "http://localhost:3000",  # your frontend URL, add more if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # allow all headers
)

app.include_router(api_router, prefix="/api/v1")