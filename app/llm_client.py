import requests
import logging
import os

from app.core.config import settings 

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/llm_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_prompt(prompt: str) -> str:
    """Отправка текста пользователем в локальную модель Ollama"""
    try:
        response = requests.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=30,
        )

        if response.status_code == 200:
            data = response.json()
            answer = data.get("response", "").strip()
            logging.info(f"Prompt: {prompt} | Response: {answer}")
            return answer
        else:
            logging.error(f"Ошибка Ollama API: {response.text}")
            return "Ошибка при обращении к Ollama API."
    except requests.exceptions.ConnectionError:
        logging.error("Ollama не запущен. Проверь, что сервер работает.")
        return "Ошибка: Ollama не запущен."
    except requests.exceptions.Timeout:
        logging.error("Таймаут запроса к Ollama.")
        return "Ошибка: время ожидания ответа истекло."
    except Exception as e:
        logging.error(f"Непредвиденная ошибка: {e}")
        return "Произошла непредвиденная ошибка."
