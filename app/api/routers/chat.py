from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import models
from app.db import schemas
from app.db.database import get_db
from app.core.security import get_current_user, auth_header

router = APIRouter()

from app.db.chat_functions import save_message, get_chat_history

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
    save_message(db=db, message=schemas.MessageCreate(user_id=current_user.user_id, session_id=token, sender_type="user", content=message.content))

    # 2. Здесь будет вызов LLM API (Google Gemini)
    # response_text = call_gemini_api(message.content, current_user.role)
    response_text = f"Заглушка ответа AI: Вы (роль: {current_user.role}) сказали '{message.content}'. Полная интеграция с LLM в разработке."

    # 3. Сохраняем ответ AI
    save_message(db=db, message=schemas.MessageCreate(user_id=current_user.user_id, session_id=token, sender_type="ai", content=response_text))

    return {"sender": "ai", "content": response_text, "timestamp": datetime.utcnow()}


@router.get("/chat/history")
async def get_chat_history(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    """
    Возвращает историю чата.
    """
    history = get_chat_history(db=db, session_id=current_user.sessions[-1].session_id)

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
            "timestamp": msg.timestamp.isoformat(),
        }
        for msg in history
    ]
