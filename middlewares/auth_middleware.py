from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any

class AuthMiddleware(BaseMiddleware):
    def __init__(self, admin_ids: list[int]):
        super().__init__()
        self.admin_ids = admin_ids

    async def __call__(self, handler: Callable, event: Message, data: Dict[str, Any]):
        """
        Проверяет, является ли пользователь администратором.
        """
        if isinstance(event, Message):
            user_id = event.from_user.id
            if user_id not in self.admin_ids:
                await event.reply("У вас нет прав для использования этого бота.")
                return  # Пропускаем обработку, если пользователь не администратор

        # Передаём управление следующему обработчику
        return await handler(event, data)
