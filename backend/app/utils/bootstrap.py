from sqlalchemy.orm import Session
from app.repos.user_repo import user_repo
from app.db.models import RoleEnum
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def bootstrap_roles(db: Session):
    role_users = {
        RoleEnum.admin: [settings.ADMIN_USER],
        RoleEnum.verifier: settings.VERIFIER_USERS.split(","),
    }

    for role, usernames in role_users.items():
        for username in usernames:
            username = username.strip()
            if not username:
                continue
            user = user_repo.get_or_create_user(db, username)
            user_repo.add_role(db, user.id, role)
            logger.info("Assigned configured role", extra={"username": username, "role": role.value})
