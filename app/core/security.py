import bcrypt
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.db import models
from app.db.database import get_db

auth_header = APIKeyHeader(name="Authorization", auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed one."""
    password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt and returns the hash as a string."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_password_bytes.decode('utf-8')


# Зависимость для получения текущего пользователя
async def get_current_user(
    token: str = Depends(auth_header), db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is missing",
        )

    # Strip "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    session = (
        db.query(models.Session)
        .filter(
            models.Session.token == token,
            models.Session.is_active == True,
            models.Session.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session token",
        )

    user = db.query(models.User).filter(models.User.user_id == session.user_id).first()
    if not user:
        # Этого не должно случиться, если сессия валидна
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
