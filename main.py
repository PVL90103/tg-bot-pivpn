import os
import asyncio
import re

import qrcode
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.types import FSInputFile, InputFile
from middlewares import AuthMiddleware, LoggingMiddleware
from dotenv import load_dotenv
from prettytable import PrettyTable


#TODO: Получение .conf файла /get <username>
#TODO: Получение информации по используемому трафику /statistics
#TODO: убрать вывод 1й строки
#TODO: Скрыть хендлеры
#TODO: Проверить запуск в контейнере

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = os.getenv('ADMIN_IDS')
CONFIG_DIR = os.getenv('CONFIG_DIR')

admin_ids = ADMIN_IDS.split(',')
admin_ids_int = [int(id) for id in admin_ids]
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.update.middleware(AuthMiddleware(admin_ids=admin_ids_int))
dp.update.middleware(LoggingMiddleware())

def remove_escape_sequences(text):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# Хэндлер на команду /clients
@dp.message(Command("clients"))
async def cmd_clients(message: types.Message):
    try:
        process = await asyncio.create_subprocess_shell(
            "pivpn clients",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            await message.reply(f"Ошибка при выполнении команды: {stderr.decode().strip()}")
            return

        output = remove_escape_sequences(stdout.decode().strip())
        lines = output.splitlines()

        connected_clients = []
        disabled_clients = []
        section = None

        for line in lines:
            if "::: Connected Clients List :::" in line:
                section = "connected"
            elif "::: Disabled clients :::" in line:
                section = "disabled"
            elif section == "connected" and not line.startswith(":::") and line.strip():
                connected_clients.append(line)
            elif section == "disabled" and not line.startswith(":::") and line.strip():
                disabled_clients.append(line)

        connected_table = PrettyTable()
        connected_table.field_names = ["Name", "Remote IP", "Virtual IP", "Bytes Received", "Bytes Sent", "Last Seen"]

        for client in connected_clients:
            columns = client.split()
            if len(columns) >= 6:
                name, remote_ip, virtual_ip, bytes_received, bytes_sent, *last_seen = columns
                last_seen = " ".join(last_seen)
                connected_table.add_row([name, remote_ip, virtual_ip, bytes_received, bytes_sent, last_seen])

        disabled_table = PrettyTable()
        disabled_table.field_names = ["Name"]

        for client in disabled_clients:
            disabled_table.add_row([client.strip()])

        response = ""
        if connected_clients:
            response += f"<b>Connected Clients:</b>\n<pre>{connected_table}</pre>\n\n"
        else:
            response += "<b>Connected Clients:</b>\n<pre>Нет активных клиентов</pre>\n\n"

        if disabled_clients:
            response += f"<b>Disabled Clients:</b>\n<pre>{disabled_table}</pre>"
        else:
            response += "<b>Disabled Clients:</b>\n<pre>Нет отключенных клиентов</pre>"

        await message.reply(response, parse_mode="HTML")

    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

# Хэндлер на команду /add
@dp.message(Command("add"))
async def cmd_add(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args and re.match("^[a-zA-Z0-9]+$", args):

            process = await asyncio.create_subprocess_shell(
                f"pivpn add -n {args}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                await message.reply(f"Ошибка при выполнении команды: {stderr.decode().strip()}")
                return

            await message.reply(f"<b>Добавлено: {args}</b>\n<pre>{stdout.decode().strip()}</pre>", parse_mode="HTML")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /add.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

# Хэндлер на команду /remove
@dp.message(Command("remove"))
async def cmd_remove(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args and re.match("^[a-zA-Z0-9]+$", args):

            process = await asyncio.create_subprocess_shell(
                f"pivpn remove {args} -y",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                await message.reply(f"Ошибка при выполнении команды: {stderr.decode().strip()}")
                return

            await message.reply(f"<b>Удаление конфига: {args}</b>\n<pre>{stdout.decode().strip()}</pre>", parse_mode="HTML")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /remove.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

# Хэндлер на команду /off
@dp.message(Command("off"))
async def cmd_off(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args and re.match("^[a-zA-Z0-9]+$", args):

            process = await asyncio.create_subprocess_shell(
                f"pivpn off {args} -y",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                await message.reply(f"Ошибка при выполнении команды: {stderr.decode().strip()}")
                return

            await message.reply(f"<b>Отключение конфига: {args}</b>\n<pre>{stdout.decode().strip()}</pre>", parse_mode="HTML")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /off.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

# Хэндлер на команду /on
@dp.message(Command("on"))
async def cmd_on(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args and re.match("^[a-zA-Z0-9]+$", args):

            process = await asyncio.create_subprocess_shell(
                f"pivpn on {args} -y",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                await message.reply(f"Ошибка при выполнении команды: {stderr.decode().strip()}")
                return

            await message.reply(f"<b>Включение конфига: {args}</b>\n<pre>{stdout.decode().strip()}</pre>", parse_mode="HTML")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /on.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

# Хэндлер на команду /qr
@dp.message(Command("qr"))
async def cmd_qr(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args and re.match("^[a-zA-Z0-9]+$", args):

            process = await asyncio.create_subprocess_shell(
                f"cat {CONFIG_DIR}/{args}.conf",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                await message.reply(f"Ошибка при выполнении команды: {stderr.decode().strip()}")
                return

            config = stdout.decode().strip()
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(config)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("qrcode.png")
            image = FSInputFile("qrcode.png")

            await message.answer_photo(image, caption="QR code для подключения")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /qr.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

# Хэндлер на команду /get
@dp.message(Command("get"))
async def cmd_get(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args and re.match("^[a-zA-Z0-9]+$", args):

            config_file = f"{CONFIG_DIR}/{args}.conf"
            if not os.path.exists(config_file):
                await message.reply(f"Файл конфигурации для клиента {args} не найден.")
                return

            file = InputFile(config_file)

            await message.reply_document(file, caption=f"Конфигурация для {args}")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /get.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
