from core.config import settings
from datetime import datetime, timedelta, UTC
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        return ph.hash(password)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        try:
            return ph.verify(hashed, password)
        except VerifyMismatchError:
            return False

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta if expires_delta else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt  
    
    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            return payload
        except jwt.InvalidTokenError:
            return None