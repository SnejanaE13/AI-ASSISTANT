from datetime import datetime
from data_base.connection import get_connection


def save_message(user_id, session_id, sender_type, content, prompt_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO Messages (user_id, session_id, sender_type, content, timestamp, prompt_id)
    VALUES (?,?,?,?,?,?);""",(
        user_id,
        session_id,
        sender_type,
        content,
        datetime.now().isoformat(),
        prompt_id))

    conn.commit()
    conn.close()


def get_chat_history(session_id, limit=20):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM Messages WHERE session_id = ? 
        ORDER BY timestamp DESC LIMIT ?
        """, (session_id, limit))

    messages = cursor.fetchall()
    conn.close()
    return messages


