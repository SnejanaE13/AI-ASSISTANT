from datetime import datetime, timedelta
from app.db import sessions, models
from app.core.config import settings


def test_create_and_get_session(db):
    session = sessions.create_session(db, user_id=1)
    assert session is not None
    assert session.session_id is not None
    assert session.is_active is True

    fetched = sessions.get_session(db, session.session_id)
    assert fetched.session_id == session.session_id


def test_delete_session(db):
    session = sessions.create_session(db, user_id=2)
    sessions.delete_session(db, session.session_id)
    fetched = sessions.get_session(db, session.session_id)
    assert fetched is None


def test_delete_expired_session(db):
    expired = models.Session(
        session_id="expired123",
        token="tkn",
        user_id=3,
        created_at=datetime.now() - timedelta(minutes=settings.SESSION_DURATION_MINUTES),
        expires_at=datetime.now() - timedelta(minutes=settings.SESSION_DURATION_MINUTES),
        is_active=True
        )
    db.add(expired)
    db.commit()

    sessions.delete_expired_sessions(db)

    result = sessions.get_session(db, "expired123")
    assert result is None


