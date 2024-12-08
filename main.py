import os

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# Хэндлер на команду /list
@dp.message(Command("list"))
async def cmd_list(message: types.Message):
    await message.reply("List")

# Хэндлер на команду /add
@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    await message.reply("Add")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
