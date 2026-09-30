import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import RoleEnum
from app.repos.user_repo import UserRepository, user_repo
from app.services.auth_service import AuthService, auth_service
from app.services.ldap_service import LdapService, ldap_service

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, repo: UserRepository, auth: AuthService, ldap_service: LdapService):
        self.repo = repo
        self.auth = auth
        self.ldap_service = ldap_service

    def login_ldap(self, db: Session, username: str, password: str) -> str:
        logger.info("Login attempt", extra={"username": username})

        if not self.ldap_service.ldap_authenticate(username, password):
            logger.warning("Login failed: invalid LDAP credentials", extra={"username": username})
            raise HTTPException(401, "Invalid credentials")

        user = self.repo.get_by_username(db, username)
        if not user:
            user = self.repo.create_user(db, username)
            self.repo.add_role(db, user.id, RoleEnum.uploader)
            logger.info("LDAP user created locally", extra={"user_id": str(user.id), "username": username})

        token = self.auth.create_access_token({"sub": str(user.id)})
        logger.info("Login successful", extra={"user_id": str(user.id), "username": username})
        return token


user_service = UserService(repo=user_repo, auth=auth_service, ldap_service=ldap_service)
