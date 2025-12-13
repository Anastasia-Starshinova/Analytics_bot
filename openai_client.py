from openai import OpenAI
import json
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


async def detect_intent(user_text: str) -> dict:
    """
    Модель возвращает строго JSON
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты помощник Telegram-бота. "
                    "Верни JSON без текста. "
                    "Возможные actions: top_videos, unknown."
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)


async def format_answer(data: list) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Сформируй понятный ответ для пользователя."
            },
            {
                "role": "user",
                "content": f"Данные: {data}"
            }
        ]
    )

    return response.choices[0].message.content