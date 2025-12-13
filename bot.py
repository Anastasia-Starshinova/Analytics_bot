import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import config
from working_with_database import create_tables, delete_table, check_tables
import os

bot = Bot(token=config.TOKEN)
dp = Dispatcher()


DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")

# delete_table(DATABASE_URL)

if check_tables(DATABASE_URL, ['videos', 'video_snapshots']) is True:
    pass
else:
    create_tables(DATABASE_URL)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я работаю на aiogram + Railway 😊")


@dp.message(Command("help"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Этот бот написан в качестве тестового задания и помогает получить данные из "
                         "базы данных :) Просто спросите то, что вам нужно и бот ответит :)")


async def main():
    print("Бот запущен и работает на Railway!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
