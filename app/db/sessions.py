from datetime import datetime, timedelta
from db.connection import get_connection
import uuid


def create_session(user_id, duration_minutes=60):
    conn = get_connection()
    cursor = conn.cursor()
    session_id = str(uuid.uuid4())
    token = str(uuid.uuid4())
    created_at = datetime.now()
    expires_at = created_at + timedelta(minutes=duration_minutes)

    cursor.execute("""
        INSERT INTO Session (session_id, token, user_id, 
        created_at, expires_at, is_active)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (session_id, token, user_id, created_at.isoformat(), expires_at.isoformat(), True))

    conn.commit()
    conn.close()
    return session_id, token


def get_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Session WHERE session_id = ?""", (session_id, ))
    session = cursor.fetchone()
    conn.close()
    return session


def delete_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" DELETE FROM Session WHERE session_id = ?
    """, (session_id, ))
    conn.commit()
    conn.close()



def delete_expired_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM Session WHERE expires_at < ? OR is_active = 0
    """, (datetime.now().isoformat(), ))
    conn.commit()
    conn.close()



