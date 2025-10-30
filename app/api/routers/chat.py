from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import models
from app.schemas import chat as schemas
from app.db.database import get_db
from app.core.security import get_current_user, auth_header

router = APIRouter()


@router.post("/chat")
async def chat_endpoint(
    message: schemas.ChatMessage,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    token: str = Depends(auth_header),
):
    """
    Обработка сообщения в чате.
    Здесь будет вызов LLM (Google Gemini).
    """
    # 1. Сохраняем сообщение пользователя
    db_message_user = models.Message(
        user_id=current_user.user_id,
        session_id=token,  # Используем токен сессии как ID
        sender_type="user",
        content=message.content,
    )
    db.add(db_message_user)

    # 2. Здесь будет вызов LLM API (Google Gemini)
    # response_text = call_gemini_api(message.content, current_user.role)
    response_text = f"Заглушка ответа AI: Вы (роль: {current_user.role}) сказали '{message.content}'. Полная интеграция с LLM в разработке."

    # 3. Сохраняем ответ AI
    db_message_ai = models.Message(
        user_id=current_user.user_id,
        session_id=token,
        sender_type="ai",
        content=response_text,
    )
    db.add(db_message_ai)
    db.commit()

    return {"sender": "ai", "content": response_text, "timestamp": datetime.utcnow()}


@router.get("/chat/history")
async def get_chat_history(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    """
    Возвращает историю чата.
    """
    history = (
        db.query(models.Message)
        .filter(models.Message.user_id == current_user.user_id)
        .order_by(models.Message.timestamp.desc())
        .limit(20)
        .all()
    )

    # Разворачиваем, чтобы были от старых к новым
    history.reverse()

    if not history:
        return [
            {
                "sender_type": "ai",
                "content": "Привет! Это начало вашей истории чата.",
                "timestamp": datetime.utcnow(),
            }
        ]

    return [
        {
            "sender_type": msg.sender_type,
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
        for msg in history
    ]
