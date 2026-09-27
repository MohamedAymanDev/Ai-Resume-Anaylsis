from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    )

    return hashed_password.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(
        password_bytes,
        hashed_bytes,
    )


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )