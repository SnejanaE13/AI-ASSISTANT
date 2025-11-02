from datetime import datetime
from data_base.connection import get_connection
import bcrypt


def create_user(first_name, last_name, second_name, role, password, email):
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("""
    INSERT INTO User (first_name, last_name, second_name, role, password_hash, created_at, email)
    VALUES (?,?,?,?,?,?,?)
    """, (first_name, last_name, second_name, role, password_hash, datetime.now().isoformat(), email))

    conn.commit()
    conn.close()


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
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return True
    else:
        return False




