from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.db import models
from app.db import schemas
from app.db.database import get_db
from app.core.security import get_current_user, auth_header
from app.llm_client import send_prompt
from anyio import to_thread

router = APIRouter()

def ensure_session_active(db: Session, current_user: models.User, token: str) -> models.Session:
    now = datetime.now(timezone.utc)

    session_obj = (
        db.query(models.Session)
        .filter(
            models.Session.token == token,
            models.Session.user_id == current_user.user_id,
            models.Session.is_active == True,
            models.Session.expires_at > now,
        )
        .first()
    )

    if not session_obj:
        raise HTTPException(status_code=401, detail="Invalid or expired session token")

    return session_obj


def build_prompt(user_role: str, user_message: str, history: list) -> str:
    base = (
        "Ты — дружелюбный ассистент по изучению иностранных языков. "
        "Отвечай кратко, понятно и по делу. "
        "Если нужно, приводи короткие примеры."
    )
    role_part = f"Роль пользователя: {user_role}." if user_role else "Роль пользователя: студент."

    history_lines = []
    for msg in history:
        sender = "Пользователь" if msg.sender_type == "user" else "Ассистент"
        history_lines.append(f"{sender}: {msg.content}")

    history_text = "\n".join(history_lines) if history_lines else "История пуста."

    return (
        f"{base}\n"
        f"{role_part}\n\n"
        f"История диалога:\n"
        f"{history_text}\n\n"
        f"Текущее сообщение пользователя: {user_message}\n\n"
        f"Сформируй полезный ответ, учитывая контекст."
    )


from app.db.chat_functions import save_message, get_chat_history as get_chat_history_from_db

@router.post("/chat")
async def chat_endpoint(
    message: schemas.ChatMessage,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    token: str = Depends(auth_header),
):
    """
    Обработка сообщения в чате.
    Здесь будет вызов LLM.
    """
        # 0. Проверяем, что сессия с таким токеном существует и активна
    session_obj = ensure_session_active(db, current_user, token)

    # 1. Сохраняем сообщение пользователя
    save_message(
        db=db,
        message=schemas.MessageCreate(
            user_id=current_user.user_id,
            session_id=session_obj.session_id,  # важно: реальный session_id из БД
            sender_type="user",
            content=message.content,
        ),
    )

    history = get_chat_history_from_db(db=db, session_id=session_obj.session_id)

    # 2. Формируем промпт для LLM
    prompt = build_prompt(current_user.role, message.content, history)

    # 3. Вызываем LLM в отдельном потоке + обработка ошибок
    try:
        response_text = await to_thread.run_sync(send_prompt, prompt)
    except Exception as e:
        # если что-то пошло совсем не так при обращении к LLM
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обращении к LLM: {e}",
        )

    if not response_text or response_text.strip() == "":
        response_text = "Модель вернула пустой ответ."

    if response_text.startswith("Ошибка:") or response_text.startswith("Произошла непредвиденная ошибка"):
        # наш llm_client вернул текст ошибки
        raise HTTPException(
            status_code=503,
            detail="Сервис генерации ответа временно недоступен. Попробуйте позже.",
        )


    # 3. Сохраняем ответ AI
    save_message(
        db=db,
        message=schemas.MessageCreate(
            user_id=current_user.user_id,
            session_id=session_obj.session_id,
            sender_type="ai",
            content=response_text,
        ),
    )

    return {"sender": "ai", "content": response_text, "timestamp": datetime.utcnow()}


@router.get("/chat/history")
async def chat_history(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    """
    Возвращает историю чата.
    """
    history = get_chat_history_from_db(db=db, session_id=current_user.sessions[-1].session_id)

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
