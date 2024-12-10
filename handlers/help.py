from aiogram import Router, types
from aiogram.filters.command import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Это бот для убравления WireGuard туннелями на сервере через утилиту PiVPN. Через команду /help ты можешь увидеть доступные команды.")

@router.message(Command("help"))
async def cmd_start(message: types.Message):
    await message.answer("Commands:\n"
                         "/clients - вывод всех клиентов\n"
                         "/add <name> - добавление нового клиента\n"
                         "/remove <name> - полное удаление конфигов клиента\n"
                         "/off <name> - отключение клиента, без удаления конфигов\n"
                         "/on <name> - включение клиента\n"
                         "/qr <name> - Получение QR кода для подключения клиента\n"
                         "/get <name> - Получение конфиг файла для подключения клиента\n")
