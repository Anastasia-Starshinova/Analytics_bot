import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import config
from working_with_database import create_tables, delete_table, check_tables
from db import get_pool, get_top_videos
from openai_client import detect_intent, format_answer
# import os

bot = Bot(token=config.TOKEN)
dp = Dispatcher()

db_pool = None

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
async def cmd_start(message: types.Message):
    await message.answer("Привет! Этот бот написан в качестве тестового задания и помогает получить данные из "
                         "базы данных :) Просто спросите то, что вам нужно и бот ответит :)")


@dp.message()
async def handle_text(message: types.Message):
    intent = await detect_intent(message.text)

    if intent.get("action") == "top_videos":
        rows = await get_top_videos(db_pool, limit=5)
        answer = await format_answer(rows)
        await message.answer(answer)
    else:
        await message.answer("Я пока не понял запрос и не знаю, что сказать 👀\nПопробуйте спросить ещё раз :)")


# async def main():
#     global db_pool
#     db_pool = await get_pool(config.DATABASE_URL)
#
#     print("🤖 Бот запущен и работает")
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
