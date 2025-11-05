from datetime import datetime
from db.connection import get_connection
import bcrypt


def create_user(first_name, last_name, second_name, role, password, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT user_id FROM User WHERE email = ?""", (email,))
    if cursor.fetchone():
        conn.close()
        raise ValueError("Пользователь с таким email уже существует")
    
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("""
    INSERT INTO User (first_name, last_name, second_name, role, password_hash, created_at, email)
    VALUES (?,?,?,?,?,?,?)
    """, (first_name, last_name, second_name, role, password_hash, datetime.now().isoformat(), email))

    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return user_id


def get_user_by_username(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM User WHERE email = ?;""", (email,))
    user = cursor.fetchone()

    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM User WHERE user_id = ?;""", (user_id, ))
    user = cursor.fetchone()

    conn.close()
    return user


def verify_password(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""SELECT password_hash FROM User WHERE email = ?""", email)
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return False

    stored_hash = result[0]
    
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')
    
    try:
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    except Exception as e:
        print(f"Ошибка при проверке пароля: {e}")
        return False




