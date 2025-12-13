from openai import OpenAI
import json
from config import OPENAI_API_KEY
import openai
import config

# client = OpenAI(api_key=OPENAI_API_KEY)

openai.api_key = config.OPENAI_API_KEY


async def detect_intent(text: str) -> dict:
    """
    Определяет intent пользователя и параметры с помощью GPT.
    Возвращает словарь {"action": str, "params": dict}.
    """
    prompt = f"""
Ты - помощник для бота Telegram, который работает с двумя таблицами в PostgreSQL:
- videos (id, creator_id, video_created_at, views_count, likes_count, comments_count, reports_count)
- video_snapshots (id, video_id, snapshot_created_at, views_count, likes_count, comments_count)

Определи действие пользователя и параметры для запроса к базе.

Верни JSON в формате:
{{
    "action": "<тип действия: total_videos, top_likes, videos_by_creator, views_above_threshold, snapshot_max_views, 
    snapshot_by_video>",
    "params": {{
        "<имя_параметра>": "<значение>"
    }}
}}

Если не можешь понять запрос, верни:
{{
    "action": "unknown",
    "params": {{}}
}}

Пользовательский вопрос: "{text}"
"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    # Получаем текст от модели
    answer_text = response.choices[0].message.content.strip()

    import json
    try:
        intent = json.loads(answer_text)
    except json.JSONDecodeError:
        # Если GPT вернул невалидный JSON
        intent = {"action": "unknown", "params": {}}

    return intent

