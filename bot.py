import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import config
from db import get_pool, query_database
from openai_client import detect_intent
# import os
import state

bot = Bot(token=config.TOKEN)
dp = Dispatcher()


DATABASE_URL = config.DATABASE_URL

# delete_table(DATABASE_URL)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! 🦄\n"
        "Спросите меня, что бы вы хотели узнать у базы данных :)\nНапример:\n"
        "• Сколько всего видео есть в системе? \n"
        "• Сколько видео у креатора с id ... вышло с 1 ноября 2025 по 5 ноября 2025 включительно?\n"
        "• Сколько видео набрало больше 100 000 просмотров за всё время?"
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Привет! Этот бот написан в качестве тестового задания и помогает получить данные из "
                         "базы данных :) Просто спросите то, что вам нужно и бот ответит :)")


@dp.message()
async def handle_text(message: types.Message):
    db_pool = state.db_pool

    intent = await detect_intent(message.text)

    print("Message:", message.text)
    print("Intent:", intent)

    action = intent.get("action")
    params = intent.get("params", {})

    if action == "unknown" or not action:
        await message.answer("Я пока не понял запрос 👀")
        return

    number = await query_database(db_pool, action, params)
    await message.answer(f"{number}")
