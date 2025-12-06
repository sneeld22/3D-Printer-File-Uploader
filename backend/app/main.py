from fastapi import FastAPI
from app.api.v1 import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.db.models import User, UserRole, RoleEnum
from app.core.config import settings
import uuid

def create_admin():
    db = SessionLocal()
    if not db.query(User).filter(User.username == settings.ADMIN_USER).first():
        admin = User(
            id=uuid.uuid4(),
            username=settings.ADMIN_USER,
            password_hash=User.hash_password(settings.ADMIN_PASSWORD)
        )
        db.add(admin)
        db.commit()
        db.add(UserRole(user_id=admin.id, role_id=RoleEnum.admin))
        db.commit()

# Create database tables
Base.metadata.create_all(bind=engine)
create_admin()

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