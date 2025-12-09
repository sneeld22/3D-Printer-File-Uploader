from datetime import datetime, timedelta
from app.core.config import settings
from jose import jwt, JWTError
from fastapi import HTTPException

class AuthService:
    def __init__(self, secret: str, algorithm: str = "HS256", expires_minutes: int = 60):
        self.secret = secret
        self.algorithm = algorithm
        self.expires_minutes = expires_minutes
    
    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=self.expires_minutes)
        to_encode["exp"] = expire
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def verify_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
        except JWTError:
            raise HTTPException(401, "Invalid token")

        return user_id

auth_service = AuthService(secret=settings.JWT_SECRET)