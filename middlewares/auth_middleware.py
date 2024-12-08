from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Dict, Any
from middlewares.logging_middleware import logger


class AuthMiddleware(BaseMiddleware):
    def __init__(self, admin_ids: list[int]):
        super().__init__()
        self.admin_ids = admin_ids

    async def __call__(self, handler: Callable, event: Update, data: Dict[str, Any]):
        """
        Проверяет, является ли пользователь администратором.
        """
        if event.message:
            user_id = event.message.from_user.id
            logger.info(f"Пользователь {user_id} пытается выполнить команду.")
            if user_id not in self.admin_ids:
                logger.warning(f"Доступ запрещён для пользователя {user_id}.")
                await event.message.reply(f"У вас нет прав для использования этого бота. Ваш user_id: {user_id}")
                return

        return await handler(event, data)
