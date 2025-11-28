from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from app.db import models
from app.db.database import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.get("/state/{screen_name}")
async def get_screen_state(
    screen_name: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Получить сохраненное состояние для конкретного экрана пользователя
    """
    state = db.query(models.UserScreenState).filter(
        models.UserScreenState.user_id == current_user.user_id,
        models.UserScreenState.screen_name == screen_name
    ).first()
    
    if state:
        return {
            "success": True,
            "screen_name": screen_name,
            "state_data": json.loads(state.state_data)
        }
    else:
        return {
            "success": True,
            "screen_name": screen_name,
            "state_data": {}  # Пустое состояние по умолчанию
        }

@router.post("/state/{screen_name}")
async def save_screen_state(
    screen_name: str,
    state_data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Сохранить состояние для конкретного экрана пользователя
    """
    # Ищем существующее состояние
    existing_state = db.query(models.UserScreenState).filter(
        models.UserScreenState.user_id == current_user.user_id,
        models.UserScreenState.screen_name == screen_name
    ).first()
    
    if existing_state:
        # Обновляем существующее
        existing_state.state_data = json.dumps(state_data)
    else:
        # Создаем новое
        new_state = models.UserScreenState(
            user_id=current_user.user_id,
            screen_name=screen_name,
            state_data=json.dumps(state_data)
        )
        db.add(new_state)
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Состояние для экрана '{screen_name}' сохранено"
    }