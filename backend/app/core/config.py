import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool = False
    MINIO_BUCKET: str

    DATABASE_URL: str
    ADMIN_USER: str
    ADMIN_PASSWORD: str
    JWT_SECRET: str

    LDAP_SERVER: str
    LDAP_DOMAIN: str
    BASE_DN: str

    class Config:
        env_file = ".env"  # loads environment variables from .env file automatically

settings = Settings()
