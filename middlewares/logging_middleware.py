import logging
from aiogram import BaseMiddleware
from aiogram.types import Update

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Запись логов в файл
        logging.StreamHandler()          # Вывод логов в консоль
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
