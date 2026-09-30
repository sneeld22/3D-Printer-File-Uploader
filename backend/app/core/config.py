from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool = False
    MINIO_BUCKET: str

    DATABASE_URL: str
    ADMIN_USER: str
    VERIFIER_USERS: str = ""
    JWT_SECRET: str
    ROOT_PATH: str = ""

    LDAP_SERVER: str
    LDAP_DOMAIN: str
    BASE_DN: str = ""

    @field_validator("ADMIN_USER")
    @classmethod
    def admin_user_required(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("ADMIN_USER must be an LDAP username")
        return value.strip()

    @field_validator("JWT_SECRET")
    @classmethod
    def strong_jwt_secret_required(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("JWT_SECRET must contain at least 32 characters")
        return value

    class Config:
        env_file = ".env"  # loads environment variables from .env file automatically

settings = Settings()
