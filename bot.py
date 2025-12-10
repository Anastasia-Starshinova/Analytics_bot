from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я работаю на aiogram + Railway 😊")


@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")


@dp.message()
async def echo(message: types.Message):
    pass
    # await message.answer(f"Ты написал: {message.text}")
