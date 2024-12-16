import logging
from logging.handlers import TimedRotatingFileHandler
import os
import time
from aiogram import BaseMiddleware
from aiogram.types import Update

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

file_handler = TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR, "bot.log"),
    when="midnight",
    interval=1,
    backupCount=7
)

file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        file_handler,                 # Запись логов в файл
        logging.StreamHandler()       # Вывод логов в консоль

    ]
)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        """
        Основной метод Middleware, вызывается для каждого события.
        """
        try:
            logger.info(f"Получено событие: {event}")
            result = await handler(event, data)
            logger.info(f"Обработано событие: {event.update_id}, результат: {result}")
            return result
        except Exception as e:
            logger.error(f"Ошибка при обработке события {event.update_id}: {e}")
            raise
