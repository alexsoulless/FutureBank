import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from tg.config import TELEGRAM_API_KEY

bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот на aiogram.")

@dp.message()
async def echo(message: Message):
    await message.answer(f"Вы написали: {message.text}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))