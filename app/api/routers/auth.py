from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
from datetime import datetime, timedelta

from app.db import models
from app.schemas import user as schemas
from app.db.database import get_db
from app.core.security import get_password_hash, verify_password, get_current_user, auth_header

router = APIRouter()


@router.post(
    "/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя
    Проверка email и пароля (>=8 символов, как в frontend).
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


@router.post("/login", response_model=schemas.TokenResponse)
def login_for_access_token(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Авторизация пользователя.
    Возвращает UUID токен сессии.
    """
    db_user = db.query(models.User).filter(models.User.email == user_login.email).first()
    if not db_user or not verify_password(user_login.password, db_user.password_hash):
        # Блокировка на 5 мин после 3 попыток - это продвинутая фича, пока не реализована
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаем сессию
    session_token = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(days=1)  # Сессия на 1 день

    new_session = models.Session(
        token=session_token, user_id=db_user.user_id, expires_at=expires, is_active=True
    )
    db.add(new_session)
    db.commit()

    return schemas.TokenResponse(session_token=session_token, user_role=db_user.role)


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
