import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

@app.post("/")
async def main(request: Request):
    try:
        body = await request.json()
        user_text = body["request"]["original_utterance"]
    except Exception:
        return {
            "version": "1.0",
            "response": {"text": "Ошибка чтения запроса", "end_session": False}
        }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": user_text}],
        "max_tokens": 100
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=4)
        # Если DeepSeek вернул ошибку (например, 401 - неверный ключ)
        if response.status_code != 200:
            answer = f"Ошибка API: {response.status_code} - {response.text}"
        else:
            answer = response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        answer = "Превышено время ожидания от DeepSeek"
    except Exception as e:
        answer = f"Ошибка на сервере: {str(e)}"

    return {
        "version": "1.0",
        "response": {
            "end_session": False,
            "text": answer,
            "tts": answer
        }
    }
