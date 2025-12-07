# app/services/user_service.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import User, RoleEnum
from app.repos.user_repo import user_repo, UserRepository
from app.services.auth_service import auth_service, AuthService

class UserService:
    def __init__(self, repo: UserRepository, auth: AuthService):
        self.repo = repo
        self.auth = auth

    def register_user(self, db: Session, username: str, password: str) -> User:
        # check if user exists
        existing = self.repo.get_by_username(db, username)
        if existing:
            raise HTTPException(400, "Username already exists")

        # hash password
        hashed = User.hash_password(password)

        # create user
        user = self.repo.create_user(db, username, hashed)

        # assign default role
        self.repo.add_role(db, user.id, RoleEnum.uploader)

        return user

    def login(self, db: Session, username: str, password: str) -> str:
        user = self.repo.get_by_username(db, username)
        if not user or not user.verify_password(password):
            raise HTTPException(401, "Invalid credentials")

        # use injected AuthService, not static method
        return self.auth.create_access_token({"sub": str(user.id)})


user_service = UserService(
    repo=user_repo,
    auth=auth_service
)
