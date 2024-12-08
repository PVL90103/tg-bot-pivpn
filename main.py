import os

import asyncio
import subprocess

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
dp.update.middleware(AuthMiddleware(admin_ids=admin_ids_int))
dp.update.middleware(LoggingMiddleware())

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# Хэндлер на команду /clients
@dp.message(Command("clients"))
async def cmd_clients(message: types.Message):
    try:
        result = subprocess.run(["pivpn", "-c"], capture_output=True, text=True)

        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                await message.reply(f"<b>Список конфигураций:</b>\n<pre>{output}</pre>", parse_mode="HTML")
            else:
                await message.reply("Нет доступных конфигураций.")
        else:
            await message.reply("Ошибка при выполнении команды `pivpn -l`.\nПроверьте настройки.")

    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

# Хэндлер на команду /add
@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    await message.reply("Add")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
