import openai
import config
import json
import anyio

client = openai.OpenAI(api_key=config.OPENAI_API_KEY)


def detect_intent_sync(text: str) -> dict:
    """
    Определяет intent пользователя и параметры с помощью GPT.
    Возвращает словарь {"action": str, "params": dict}.
    """
    prompt = f"""
Ты - помощник для бота Telegram, который работает с двумя таблицами в PostgreSQL:
- videos (id, creator_id, video_created_at, views_count, likes_count, comments_count, reports_count, created_at,
updated_at)
- video_snapshots (id, video_id, views_count, likes_count, comments_count, reports_count, delta_views_count, 
delta_likes_count, delta_comments_count, delta_reports_count, created_at, updated_at)

Определи действие пользователя и параметры для запроса к базе.

Верни JSON в формате:
{{
    "action": "<тип действия: total_videos, top_likes, videos_by_creator, views_above_threshold, snapshot_max_views, 
    snapshot_by_video, sum_views_by_date, creator_videos_views_final>",
    "params": {{
        "date": "YYYY-MM-DD",
        "creator_id": "<id>",
        "video_id": "<id>",
        "threshold": <число>
    }}
}}

Важно: Если запрос про "итоговую статистику" или "по итоговой статистике" для видео креатора с просмотрами выше порога, 
используй действие "creator_videos_views_final". Это действие берет максимальное значение views_count из video_snapshots 
для каждого видео (итоговая статистика).

Если не можешь понять запрос, верни:
{{
    "action": "unknown",
    "params": {{}}
}}

Пользовательский вопрос: "{text}"
"""

    # Синхронный вызов
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    answer_text = response.choices[0].message.content.strip()

    try:
        intent = json.loads(answer_text)
    except json.JSONDecodeError:
        intent = {"action": "unknown", "params": {}}

    return intent


# Если используете FastAPI / aiogram и нужно асинхронно:


async def detect_intent(text: str) -> dict:
    return await anyio.to_thread.run_sync(detect_intent_sync, text)

