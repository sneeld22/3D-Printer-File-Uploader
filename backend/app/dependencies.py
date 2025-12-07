from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.db.models import User
from app.core.config import settings
from app.db.session import SessionLocal
from app.services.auth_service import AuthService
from sqlalchemy.orm import joinedload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    user_id = AuthService.verify_token(token)
    user = db.query(User).options(joinedload(User.roles)).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    return user