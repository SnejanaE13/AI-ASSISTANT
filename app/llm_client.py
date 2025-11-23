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
    """Отправка текста в LLM (Ollama или OpenRouter в зависимости от USE_OPENROUTER)"""
    try:
        if settings.USE_OPENROUTER:
            if not settings.OPENROUTER_API_KEY.strip():
                logging.error("OPENROUTER_API_KEY не настроен.")
                return "Ошибка: OPENROUTER_API_KEY не настроен в .env"

            url = f"{settings.OPENROUTER_BASE_URL}/chat/completions"
            headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ultron-assistant.local",  # Optional
                "X-Title": "Ultron Learning Assistant",  # Optional
            }
            data = {
                "model": settings.OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}],
            }
            response = requests.post(url, headers=headers, json=data, timeout=60)

            if response.status_code == 200:
                api_data = response.json()
                answer = api_data["choices"][0]["message"]["content"].strip()
                logging.info(
                    f"OpenRouter | Model: {settings.OPENROUTER_MODEL} | "
                    f"Prompt: {prompt[:150]}... | Response: {answer[:150]}..."
                )
                return answer
            else:
                logging.error(f"OpenRouter API {response.status_code}: {response.text[:300]}")
                return "Ошибка при обращении к OpenRouter API."
        else:
            # Ollama
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
                logging.info(
                    f"Ollama | Model: {settings.OLLAMA_MODEL} | "
                    f"Prompt: {prompt[:150]}... | Response: {answer[:150]}..."
                )
                return answer
            else:
                logging.error(f"Ошибка Ollama API: {response.text}")
                return "Ошибка при обращении к Ollama API."

    except requests.exceptions.ConnectionError as e:
        backend = "OpenRouter" if settings.USE_OPENROUTER else "Ollama"
        logging.error(f"{backend} connection error: {e}")
        return f"Ошибка: {backend} не доступен."
    except requests.exceptions.Timeout:
        logging.error("Таймаут запроса.")
        return "Ошибка: время ожидания ответа истекло."
    except KeyError as e:
        logging.error(f"Неверный формат ответа API: {e}")
        return "Ошибка обработки ответа LLM."
    except Exception as e:
        logging.error(f"Непредвиденная ошибка: {e}")
        return "Произошла непредвиденная ошибка."
