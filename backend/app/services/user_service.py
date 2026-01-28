from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import User, RoleEnum
from app.repos.user_repo import user_repo, UserRepository
from app.services.auth_service import auth_service, AuthService
from app.services.ldap_service import ldap_service, LdapService

import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, repo: UserRepository, auth: AuthService, ldap_service: LdapService):
        self.repo = repo
        self.auth = auth
        self.ldap_service = ldap_service

    def register_user(self, db: Session, username: str, password: str) -> User:
        logger.info(
            "User registration attempt",
            extra={"username": username},
        )
        existing = self.repo.get_by_username(db, username)
        if existing:
            logger.warning(
                "User registration failed: username exists",
                extra={"username": username},
            )
            raise HTTPException(400, "Username already exists")

        hashed = User.hash_password(password)

        user = self.repo.create_user(db, username, hashed)

        # assign default role
        self.repo.add_role(db, user.id, RoleEnum.uploader)

        logger.info(
            "User registered successfully",
            extra={"user_id": str(user.id), "username": username},
        )

        return user

    def login(self, db: Session, username: str, password: str) -> str:

        logger.info(
            "Login attempt",
            extra={"username": username},
        )

        user = self.repo.get_by_username(db, username)
        if not user or not user.verify_password(password):
            logger.warning(
                "Login failed: invalid credentials",
                extra={"username": username},
            )
            raise HTTPException(401, "Invalid credentials")

        token = self.auth.create_access_token({"sub": str(user.id)})

        logger.info(
            "Login successful",
            extra={"user_id": str(user.id), "username": username},
        )
        
        return token
    

    def login_ldap(self, db: Session, username: str, password: str) -> str:
        logger.info(
            "Login attempt",
            extra={"username": username},
        )
        
        # Try LDAP authentication first
        if ldap_service.ldap_authenticate(username, password):
            # Check if user exists locally, if not, create a basic user record
            user = self.repo.get_by_username(db, username)
            if not user:
                # Create user with a placeholder password (won't be used)
                user = self.repo.create_user(db, username)
                # Assign default role
                self.repo.add_role(db, user.id, RoleEnum.uploader)

                logger.info(
                    "LDAP user created locally",
                    extra={"user_id": str(user.id), "username": username},
                )
        else:
            logger.warning(
                "Login failed: invalid LDAP credentials",
                extra={"username": username},
            )
            raise HTTPException(401, "Invalid credentials")

        token = self.auth.create_access_token({"sub": str(user.id)})

        logger.info(
            "Login successful",
            extra={"user_id": str(user.id), "username": username},
        )

        return token


user_service = UserService(
    repo=user_repo,
    auth=auth_service,
    ldap_service=ldap_service
)
