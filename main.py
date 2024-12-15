import os
import asyncio

from aiogram import Bot, Dispatcher
from middlewares import AuthMiddleware, LoggingMiddleware, ConfigMiddleware
from dotenv import load_dotenv
from handlers import help, commands

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = os.getenv('ADMIN_IDS')
CONFIG_DIR = os.getenv('CONFIG_DIR')


async def main():
    admin_ids = ADMIN_IDS.split(',')
    admin_ids_int = [int(id) for id in admin_ids]
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.update.middleware(AuthMiddleware(admin_ids=admin_ids_int))
    dp.update.middleware(LoggingMiddleware())

    dp.include_router(help.router)
    dp.include_router(commands.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
