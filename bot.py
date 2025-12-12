import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import config
from working_with_database import create_table, delete_table
import os

bot = Bot(token=config.TOKEN)
dp = Dispatcher()


DATABASE_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://")

# create_table(DATABASE_URL)


# delete_table(DATABASE_URL)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я работаю на aiogram + Railway 😊")


async def main():
    print("Бот запущен и работает на Railway!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
