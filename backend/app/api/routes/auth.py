from fastapi import APIRouter, Depends
from app.schemas.auth import UserCreate, UserLogin, UserOut
from app.dependencies import get_current_user, get_db
from app.services.user_service import user_service
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = user_service.register_user(db, payload.username, payload.password)
    return user

@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    token = user_service.login(db, payload.username, payload.password)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(user = Depends(get_current_user)):
    return user