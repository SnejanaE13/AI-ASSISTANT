import requests
import json
import time

API_URL = "http://127.0.0.1:8000"

def test_register_user(email, password, first_name, last_name, role):
    user_data = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "role": role,
    }

    try:
        response = requests.post(f"{API_URL}/api/register", json=user_data)
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(response.text)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        print("Please make sure the FastAPI server is running.")

if __name__ == "__main__":
    # Генерируем уникальный идентификатор для каждого запуска теста
    unique_id = int(time.time())
    
    print("--- Testing with a valid 9-character password ---")
    test_register_user(
        email=f"testuser1_{unique_id}@example.com",
        password="password1",
        first_name="Тест",
        last_name="Пользователь1",
        role="student",
    )

    print("\n--- Testing with a long password (more than 72 characters) ---")
    long_password = "a" * 73
    test_register_user(
        email=f"testuser2_{unique_id}@example.com",
        password=long_password,
        first_name="Тест",
        last_name="Пользователь2",
        role="student",
    )

    print("\n--- Testing with a 9-character Cyrillic password ---")
    test_register_user(
        email=f"testuser3_{unique_id}@example.com",
        password="пароль123",
        first_name="Тест",
        last_name="Пользователь3",
        role="student",
    )
