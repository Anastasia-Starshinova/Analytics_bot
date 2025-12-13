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
- video_snapshots (id, video_id, views_count, likes_count, comments_count, reports_count,
  delta_views_count, delta_likes_count, delta_comments_count, delta_reports_count, created_at, updated_at)

Твоя задача — определить действие (action) и параметры (params) для запроса к базе данных.

### Возможные действия (action):

- total_videos  
- total_snapshots  
- top_likes  
- videos_by_creator  
- views_above_threshold  
- snapshot_max_views  
- snapshot_by_video  
- sum_views_by_date  
- creator_videos_views_final  

- negative_view_snapshots  
  Используется, когда пользователь спрашивает:
  - сколько замеров статистики
  - где просмотры уменьшились
  - где число просмотров стало меньше по сравнению с предыдущим замером
  - где delta просмотров отрицательная  
  ⚠️ считается КОЛИЧЕСТВО ЗАМЕРОВ

- sum_views_by_video_publish_date  
  Используется, когда пользователь спрашивает:
  - суммарное количество просмотров всех видео
  - просмотры видео, опубликованных за месяц или период  
  📌 Суммируется videos.views_count  
  📌 Фильтр по videos.video_created_at  
  📌 Если указан месяц — используй start_date и end_date

- creator_delta_views_in_time_range  
  Используется, когда пользователь спрашивает:
  - на сколько просмотров выросли видео
  - суммарный рост просмотров
  - сложить изменения просмотров
  - прирост просмотров между замерами
  - за период времени в течение дня
  - по замерам статистики

  📌 Суммируется: video_snapshots.delta_views_count  
  📌 Фильтрация:
  - по creator_id (через videos.id → video_snapshots.video_id)
  - по дате (video_snapshots.created_at::date)
  - по временному интервалу (created_at::time BETWEEN start_time AND end_time)

⚠️ ОБЯЗАТЕЛЬНО:
- Если в вопросе указан интервал времени (например 10:00–15:00),
  ты ОБЯЗАН вернуть параметры start_time и end_time в формате HH:MM
- Если указана конкретная дата, ты ОБЯЗАН вернуть параметр date в формате YYYY-MM-DD
- Для действия creator_delta_views_in_time_range все параметры
  (creator_id, date, start_time, end_time) ОБЯЗАТЕЛЬНЫ

---

Верни JSON в формате:
{{
    "action": "<тип действия: total_videos, total_snapshots, top_likes, videos_by_creator,
               views_above_threshold, snapshot_max_views, snapshot_by_video,
               sum_views_by_date, sum_views_by_video_publish_date,
               creator_videos_views_final, negative_view_snapshots>",
    "params": {{
        "date": "YYYY-MM-DD",
        "start_time": "HH:MM",
        "end_time": "HH:MM",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD",
        "creator_id": "<id>",
        "video_id": "<id>",
        "threshold": <число>
    }}
}}

Важно:
- Если вопрос про *рост / изменение / прирост просмотров* — всегда используй delta_views_count
- Если указан интервал времени внутри дня — используй start_time и end_time
- Если указан креатор — обязательно передай creator_id
- Если запрос про "итоговую статистику" или "по итоговой статистике" для видео креатора с просмотрами выше порога, 
  используй действие "creator_videos_views_final". Это действие берет максимальное значение views_count 
  из video_snapshots для каждого видео (итоговая статистика).

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

