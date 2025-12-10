from fastapi import FastAPI, Request
from bot import bot, dp
import config
import asyncio

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(config.WEBHOOK_URL)


@app.post(config.WEBHOOK_PATH)
async def webhook(request: Request):
    update = await request.json()
    await dp.feed_webhook_update(bot, update)
    return {"status": "ok"}


@app.get("/")
async def index():
    return {"status": "Bot is running on Railway!"}

