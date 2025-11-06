from sqlalchemy.orm import Session
from . import models, schemas

def save_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_chat_history(db: Session, session_id: str, limit: int = 20):
    return db.query(models.Message).filter(models.Message.session_id == session_id).order_by(models.Message.timestamp.desc()).limit(limit).all()


