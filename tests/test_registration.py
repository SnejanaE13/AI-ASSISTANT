import requests
import json
import time
import pytest

API_URL = "http://127.0.0.1:8000"

def _register_user_helper(email, password, first_name, last_name, role):
    user_data = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "role": role,
    }

    try:
        response = requests.post(f"{API_URL}/api/register", json=user_data)
        # Optional: print response details for debugging
        # print(f"Status Code: {response.status_code}")
        # print("Response JSON:")
        # try:
        #     print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        # except json.JSONDecodeError:
        #     print(response.text)
        return response

    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
        print("Please make sure the FastAPI server is running.")
        pytest.fail(f"Could not connect to FastAPI server: {e}")


def test_valid_8_char_password_registration():
    unique_id = int(time.time())
    response = _register_user_helper(
        email=f"testuser_valid_{unique_id}@example.com",
        password="password",
        first_name="Тест",
        last_name="Валидный",
        role="student",
    )
    assert response.status_code == 201


def test_long_password_registration_too_long():
    unique_id = int(time.time())
    long_password = "a" * 73  # More than 72 bytes (assuming ASCII)
    response = _register_user_helper(
        email=f"testuser_long_{unique_id}@example.com",
        password=long_password,
        first_name="Тест",
        last_name="Длинный",
        role="student",
    )
    assert response.status_code == 422  # Expect validation error
    assert "detail" in response.json()
    assert "Пароль не может превышать 72 байта" in response.json()["detail"][0]["msg"]


def test_cyrillic_password_registration_too_long():
    unique_id = int(time.time())
    # Cyrillic characters are multi-byte, 9 Cyrillic chars will be > 72 bytes
    cyrillic_password_too_long = "приветмирприветмирприветмирприветмирприветмирприветмирприветмирприветмир" # 56 chars, ~112 bytes
    response = _register_user_helper(
        email=f"testuser_cyrillic_long_{unique_id}@example.com",
        password=cyrillic_password_too_long,
        first_name="Тест",
        last_name="Кириллица",
        role="student",
    )
    assert response.status_code == 422
    assert "detail" in response.json()
    assert "Пароль не может превышать 72 байта" in response.json()["detail"][0]["msg"]


def test_password_less_than_8_chars():
    unique_id = int(time.time())
    response = _register_user_helper(
        email=f"testuser_short_{unique_id}@example.com",
        password="short", # 5 characters
        first_name="Тест",
        last_name="Короткий",
        role="student",
    )
    assert response.status_code == 422
    assert "detail" in response.json()
    assert "String should have at least 8 characters" in response.json()["detail"][0]["msg"]