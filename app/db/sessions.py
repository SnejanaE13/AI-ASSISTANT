from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta
import uuid

def create_session(db: Session, user_id: int, duration_minutes: int = 60) -> models.Session:
    session_id = str(uuid.uuid4())
    token = str(uuid.uuid4())
    created_at = datetime.now()
    expires_at = created_at + timedelta(minutes=duration_minutes)
    db_session = models.Session(
        session_id=session_id,
        token=token,
        user_id=user_id,
        created_at=created_at,
        expires_at=expires_at,
        is_active=True
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session(db: Session, session_id: str) -> models.Session:
    return db.query(models.Session).filter(models.Session.session_id == session_id).first()

def delete_session(db: Session, session_id: str):
    db_session = db.query(models.Session).filter(models.Session.session_id == session_id).first()
    if db_session:
        db.delete(db_session)
        db.commit()

def delete_expired_sessions(db: Session):
    db.query(models.Session).filter(models.Session.expires_at < datetime.now()).delete()
    db.commit()



