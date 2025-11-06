import requests
import logging
import os

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
            "http://localhost:11434/api/generate",
            json={"model": "gpt-oss:20b", "prompt": prompt, "stream": False},
            timeout=120
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
