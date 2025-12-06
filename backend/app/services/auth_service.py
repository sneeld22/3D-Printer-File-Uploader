from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

SECRET = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class AuthService:
    @staticmethod
    def create_access_token(data: dict, expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=expires_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)