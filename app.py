from fastapi import FastAPI, Request
from bot import bot, dp, DATABASE_URL
from db import get_pool
from working_with_database import create_tables, check_tables
import config
from aiogram.types import Update
import state


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    state.db_pool = await get_pool(DATABASE_URL)

    if not check_tables(DATABASE_URL, ['videos', 'video_snapshots']):
        create_tables(DATABASE_URL)

    await bot.set_webhook(config.WEBHOOK_URL)
    print("🤖 Webhook установлен, бот запущен")


@app.post(config.WEBHOOK_PATH)
async def webhook(request: Request):
    update = Update(**await request.json())
    await dp.process_update(update)
    return {"ok": True}


@app.get("/")
async def index():
    return {"status": "Bot is running on Railway!"}

