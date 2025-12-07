from fastapi import APIRouter, Depends, HTTPException
from app.db.models import User, UserRole, RoleEnum
from app.schemas.auth import UserCreate, UserLogin, UserOut
from app.services.auth_service import AuthService
from app.dependencies import get_current_user, get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(400, "Username already exists")

    new_user = User(
        username=user.username,
        password_hash=User.hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    role = UserRole(user_id=new_user.id, role_id=RoleEnum.uploader)
    db.add(role)
    db.commit()

    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(401, "Invalid credentials")

    token = AuthService.create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user