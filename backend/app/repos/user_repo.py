from sqlalchemy.orm import Session
from app.db.models import User, UserRole, RoleEnum

class UserRepository:
    def get_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def get_by_id(self, db: Session, user_id: str) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def create_user(self, db: Session, username: str, password_hash: str) -> User:
        user = User(username=username, password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def add_role(self, db: Session, user_id: str, role: RoleEnum):
        user_role = UserRole(user_id=user_id, role_id=role)
        db.add(user_role)
        db.commit()

user_repo = UserRepository()