"""
Скрипт для тестирования работы базы данных
"""
from db.connection import get_connection
from db.schema import create_db
from db.CRUD import create_user, get_user_by_username, verify_password
from db.sessions import create_session, get_session, validate_session, delete_expired_sessions
from db.chat_functions import save_message, get_chat_history, get_user_chat_sessions
import os


def test_database():
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ БАЗЫ ДАННЫХ")
    print("=" * 60)
    
    # 1. Создание базы данных
    print("\n1. Создание базы данных...")
    try:
        create_db()
        print("✓ База данных создана успешно")
    except Exception as e:
        print(f"✗ Ошибка при создании БД: {e}")
        return
    
    # 2. Регистрация пользователя
    print("\n2. Тестирование регистрации...")
    try:
        user_id = create_user(
            first_name="Иван",
            last_name="Иванов",
            second_name="Иванович",
            role="user",
            password="test_password_123",
            email="ivan@test.com"
        )
        print(f"✓ Пользователь создан с ID: {user_id}")
    except Exception as e:
        print(f"✗ Ошибка при создании пользователя: {e}")
        # Возможно, пользователь уже существует
        user = get_user_by_username("ivan@test.com")
        if user:
            user_id = user[0]
            print(f"  Используем существующего пользователя с ID: {user_id}")
        else:
            return
    
    # 3. Проверка авторизации
    print("\n3. Тестирование авторизации...")
    try:
        # Правильный пароль
        if verify_password("ivan@test.com", "test_password_123"):
            print("✓ Авторизация с правильным паролем успешна")
        else:
            print("✗ Авторизация с правильным паролем не прошла")
        
        # Неправильный пароль
        if not verify_password("ivan@test.com", "wrong_password"):
            print("✓ Авторизация с неправильным паролем корректно отклонена")
        else:
            print("✗ Авторизация с неправильным паролем прошла (ошибка!)")
    except Exception as e:
        print(f"✗ Ошибка при проверке пароля: {e}")
        return
    
    # 4. Создание сессии
    print("\n4. Тестирование сессий...")
    try:
        session_id, token = create_session(user_id, duration_minutes=60)
        print(f"✓ Сессия создана: {session_id}")
        print(f"  Token: {token[:20]}...")
        
        # Проверка валидности сессии
        if validate_session(session_id):
            print("✓ Сессия валидна")
        else:
            print("✗ Сессия невалидна")
    except Exception as e:
        print(f"✗ Ошибка при создании сессии: {e}")
        return
    
    # 5. Работа с сообщениями
    print("\n5. Тестирование сохранения сообщений...")
    try:
        # Сообщение от пользователя
        msg_id_1 = save_message(
            user_id=user_id,
            session_id=session_id,
            sender_type="user",
            content="Привет! Как дела?"
        )
        print(f"✓ Сообщение пользователя сохранено (ID: {msg_id_1})")
        
        # Ответ ассистента
        msg_id_2 = save_message(
            user_id=user_id,
            session_id=session_id,
            sender_type="assistant",
            content="Здравствуйте! У меня всё хорошо. Чем могу помочь?"
        )
        print(f"✓ Ответ ассистента сохранен (ID: {msg_id_2})")
        
        # Ещё одно сообщение
        msg_id_3 = save_message(
            user_id=user_id,
            session_id=session_id,
            sender_type="user",
            content="Расскажи о погоде"
        )
        print(f"✓ Второе сообщение пользователя сохранено (ID: {msg_id_3})")
    except Exception as e:
        print(f"✗ Ошибка при сохранении сообщений: {e}")
        return
    
    # 6. Получение истории чата
    print("\n6. Тестирование получения истории чата...")
    try:
        history = get_chat_history(session_id, limit=10)
        print(f"✓ Получено сообщений: {len(history)}")
        print("\nИстория чата:")
        for msg in history:
            sender = "👤 User" if msg[3] == "user" else "🤖 Assistant"
            content = msg[4][:50] + "..." if len(msg[4]) > 50 else msg[4]
            print(f"  {sender}: {content}")
    except Exception as e:
        print(f"✗ Ошибка при получении истории: {e}")
        return
    
    # 7. Получение списка сессий пользователя
    print("\n7. Тестирование получения списка сессий...")
    try:
        sessions = get_user_chat_sessions(user_id, limit=5)
        print(f"✓ Найдено сессий: {len(sessions)}")
        for sess in sessions:
            preview = sess[2][:40] + "..." if sess[2] and len(sess[2]) > 40 else sess[2]
            print(f"  Session: {sess[0][:20]}... | Last: {sess[1]} | Preview: {preview}")
    except Exception as e:
        print(f"✗ Ошибка при получении сессий: {e}")
    
    # 8. Проверка структуры БД
    print("\n8. Проверка структуры базы данных...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"✓ Таблицы в БД: {', '.join([t[0] for t in tables])}")
        
        # Проверяем количество записей
        cursor.execute("SELECT COUNT(*) FROM User")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Session")
        session_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Messages")
        message_count = cursor.fetchone()[0]
        
        print(f"  Пользователей: {user_count}")
        print(f"  Сессий: {session_count}")
        print(f"  Сообщений: {message_count}")
        
        conn.close()
    except Exception as e:
        print(f"✗ Ошибка при проверке структуры: {e}")
    
    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 60)


if __name__ == "__main__":
    test_database()