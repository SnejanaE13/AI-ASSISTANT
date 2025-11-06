from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import uuid
from datetime import datetime, timedelta, timezone
import os
import logging
import redis
from redis.exceptions import RedisError
from app.db import models
from app.db import schemas
from app.db.database import get_db
from app.core.security import get_password_hash, verify_password, get_current_user, auth_header

router = APIRouter()

logger = logging.getLogger(__name__)

# Redis setup for login rate limiting. Uses REDIS_URL env var if present.
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
try:
    redis_client = redis.from_url(REDIS_URL)
    # quick health-check
    redis_client.ping()
except Exception as e:
    redis_client = None
    logger.warning("Redis not available for login rate limiting: %s", e)

@router.post(
    "/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя
    Проверка email и пароля (>=9 символов, как в frontend).
    """
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )

    hashed_password = get_password_hash(user.password)
        
    new_user = models.User(
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        second_name=user.second_name,
        role=user.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


from app.db.sessions import create_session

@router.post("/login", response_model=schemas.TokenResponse)
def login_for_access_token(user_login: schemas.UserLogin, db: Session = Depends(get_db), request: Request = None):
    """
    Авторизация пользователя.
    Возвращает UUID токен сессии.
    """
    db_user = db.query(models.User).filter(models.User.email == user_login.email).first()
    client_ip = None
    try:
        if request and request.client:
            client_ip = request.client.host
    except Exception:
        client_ip = None

    key = f"login:fail:{user_login.email}"
    if client_ip:
        key = f"{key}:{client_ip}"

    if redis_client is not None:
        try:
            val = redis_client.get(key)
            if val is not None:
                try:
                    fails = int(val)
                except Exception:
                    fails = 0
                if fails >= 3:
                    try:
                        ttl = redis_client.ttl(key)
                    except RedisError as e:
                        ttl = None
                        logger.warning("Redis error while fetching TTL for %s: %s", key, e)

                    if ttl is None:
                        ttl_display = "unknown"
                    elif ttl <= 0:
                        ttl_display = "no expiry"
                    else:
                        ttl_display = ttl

                    logger.info(
                        "Login blocked for %s (email=%s, ip=%s) — %d failed attempts, ttl=%s",
                        key,
                        user_login.email,
                        client_ip,
                        fails,
                        ttl_display,
                    )

                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Неверный email или пароль",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
        except RedisError as e:
            logger.warning("Redis error while checking login attempts for %s: %s", key, e)
        except Exception as e:
            logger.exception("Unexpected error while checking login attempts for %s: %s", key, e)
    if not db_user or not verify_password(user_login.password, db_user.password_hash):
        # Блокировка на 5 мин после 3 попыток - это продвинутая фича, пока не реализована
        if redis_client is not None:
            try:
                new = redis_client.incr(key)
                if new == 1:
                    redis_client.expire(key, 300)
                logger.info("Failed login attempt for %s (email=%s, ip=%s). Count=%s", key, user_login.email, client_ip, new)
            except RedisError as e:
                logger.warning("Redis error while incrementing login attempts for %s: %s", key, e)
            except Exception:
                logger.exception("Unexpected error while incrementing login attempts for %s", key)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if redis_client is not None:
        try:
            redis_client.delete(key)
        except RedisError as e:
            logger.warning("Redis error while deleting login attempts key %s: %s", key, e)
        except Exception:
            logger.exception("Unexpected error while deleting login attempts key %s", key)

    # Создаем сессию
    new_session = create_session(db=db, user_id=db_user.user_id)

    return schemas.TokenResponse(session_token=new_session.token, user_role=db_user.role)


@router.post("/logout")
def logout_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    token: str = Depends(auth_header),
):
    """
    Выход из системы
    Аннулирует токен.
    """
    session = (
        db.query(models.Session)
        .filter(models.Session.token == token, models.Session.user_id == current_user.user_id)
        .first()
    )
    if session:
        session.is_active = False
        db.commit()

    return {"message": "Вы успешно вышли из системы"}
