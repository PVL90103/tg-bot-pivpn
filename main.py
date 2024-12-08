import os

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from middlewares import AuthMiddleware, LoggingMiddleware
from dotenv import load_dotenv

#TODO: Проверка, является ли пользователь администратором
#TODO: Отправка списка доступных пользователей VPN /list
#TODO: Создание нового VPN-пользователя /add <username>
#TODO: Удаление существующего VPN-пользователя /remove <username>
#TODO: Отключение пользователя /off
#TODO: Включение пользователя /on
#TODO: Удаление существующего VPN-пользователя /remove <username>
#TODO: Получение .conf файла /get <username>
#TODO: Отправка QR-кода для подключения /qr <username>
#TODO: Получение информации по используемому трафику /statistics

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = os.getenv('ADMIN_IDS')

admin_ids = ADMIN_IDS.split(',')
admin_ids_int = [int(id) for id in admin_ids]
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.middleware.setup(AuthMiddleware(admin_ids=admin_ids_int))
dp.middleware.setup(LoggingMiddleware())

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
