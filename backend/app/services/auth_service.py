from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings
from jose import jwt, JWTError
from fastapi import HTTPException

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
    
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
        except JWTError:
            raise HTTPException(401, "Invalid token")
        
        return user_id