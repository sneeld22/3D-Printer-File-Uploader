import yaml
from sqlalchemy.orm import Session
from app.repos.user_repo import user_repo
from app.db.models import RoleEnum
import logging

logger = logging.getLogger(__name__)

def bootstrap_roles(db: Session, filename: str = "app/role_bootstrap.yaml"):
    if db.query(user_repo.get_or_create_user.__annotations__['return']).count() > 0:
        return

    try:
        with open(filename) as f:
            config = yaml.safe_load(f)
    except IOError:
        logger.error(
            "Failed to open role file"
        )
        return

    for role_name, usernames in config.items():
        role = RoleEnum[role_name]
        if not role:
            continue
        for username in usernames:
            user = user_repo.get_or_create_user(db, username)
            user_repo.add_role(db, user.id, role)
