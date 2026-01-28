from pydantic import BaseModel, ConfigDict, field_validator
from app.db.models import RoleEnum
from uuid import UUID

class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    roles: list[str]

    @field_validator("roles", mode='before')
    @classmethod
    def serialize_roles(cls, roles):
        return [role.role_id.value for role in roles]