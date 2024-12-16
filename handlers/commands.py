import os
import asyncio
import re
from enum import Enum

import qrcode
from aiogram import  types, Router
from aiogram.filters.command import Command, CommandObject
from aiogram.types import FSInputFile
from prettytable import PrettyTable
from main import CONFIG_DIR

router = Router()

class ClientState(Enum):
    INIT = "init"
    CONNECTED = "connected"
    DISABLED = "disabled"

def remove_escape_sequences(text) -> str:
    '''
    Удаляем все escape-символы
    :param text: Строка
    :return: Строку без escape-символов
    '''
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

def args_validate(args: str) -> bool:
    return args and re.match("^[a-zA-Z0-9]+$", args) is not None

async def run_shell_command(cmd: str, message: types.Message):
    process = await asyncio.create_subprocess_shell(
        f"{cmd}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        await message.reply(f"Ошибка при выполнении команды: {stderr.decode().strip()}")
        return

    return stdout, stderr


@router.message(Command("clients"))
async def cmd_clients(message: types.Message):
    try:
        stdout, stderr = await run_shell_command("pivpn clients", message)

        output = remove_escape_sequences(stdout.decode().strip())
        lines = output.splitlines()

        state = ClientState.INIT

        connected_table = PrettyTable()
        connected_table.field_names = ["Name", "Remote IP", "Virtual IP", "Bytes Received", "Bytes Sent", "Last Seen"]

        disabled_table = PrettyTable()
        disabled_table.field_names = ["Name"]

        num_columns_connected = len(connected_table.field_names)
        num_columns_disabled = len(disabled_table.field_names)


        for line in lines:
            if "Name" in line and "Remote IP" in line:
                continue
            elif "::: Connected Clients List :::" in line:
                state = ClientState.CONNECTED
                continue
            elif "::: Disabled clients :::" in line:
                state = ClientState.DISABLED
                continue

            if line and state == ClientState.CONNECTED:
                if not line.startswith(":::"):
                    columns = line.split()
                    if len(columns) >= num_columns_connected:
                        name, remote_ip, virtual_ip, bytes_received, bytes_sent, *last_seen = columns
                        last_seen = " ".join(last_seen)
                        connected_table.add_row([name, remote_ip, virtual_ip, bytes_received, bytes_sent, last_seen])
            elif line and state == ClientState.DISABLED:
                if not line.startswith(":::"):
                    column = line.split()[0]
                    columns = line.strip()
                    print(column)
                    print(columns)
                    disabled_table.add_row([column])

        response = ""
        if connected_table.rows:
            response += f"<b>Connected Clients:</b>\n<pre>{connected_table}</pre>\n\n"
        else:
            response += "<b>Connected Clients:</b>\n<pre>Нет активных клиентов</pre>\n\n"

        if disabled_table.rows:
            response += f"<b>Disabled Clients:</b>\n<pre>{disabled_table}</pre>"
        else:
            response += "<b>Disabled Clients:</b>\n<pre>Нет отключенных клиентов</pre>"

        await message.reply(response, parse_mode="HTML")

    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

@router.message(Command("add"))
async def cmd_add(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args_validate(args):
            stdout, stderr = await run_shell_command(f"pivpn add -n {args}", message)
            await message.reply(f"<b>Добавлено: {args}</b>\n<pre>{stdout.decode().strip()}</pre>", parse_mode="HTML")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /add.")

    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

@router.message(Command("remove"))
async def cmd_remove(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args_validate(args):
            stdout, stderr = await run_shell_command(f"pivpn remove {args} -y", message)
            await message.reply(f"<b>Удаление конфига: {args}</b>\n<pre>{stdout.decode().strip()}</pre>", parse_mode="HTML")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /remove.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

@router.message(Command("off"))
async def cmd_off(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args_validate(args):
            stdout, stderr = await run_shell_command(f"pivpn off {args} -y", message)
            await message.reply(f"<b>Отключение конфига: {args}</b>\n<pre>{stdout.decode().strip()}</pre>", parse_mode="HTML")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /off.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

@router.message(Command("on"))
async def cmd_on(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args_validate(args):
            stdout, stderr = await run_shell_command(f"pivpn on {args} -y", message)
            await message.reply(f"<b>Включение конфига: {args}</b>\n<pre>{stdout.decode().strip()}</pre>", parse_mode="HTML")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /on.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")

@router.message(Command("qr"))
async def cmd_qr(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args_validate(args):

            config_file = f"{CONFIG_DIR}/{args}.conf"
            try:
                with open(config_file, 'r') as file:
                    config = file.read()

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

            except FileNotFoundError:
                await message.reply(f"Файл {config_file} не найден.")
            except PermissionError:
                await message.reply(f"Нет разрешения на чтение файла {config_file}")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /qr.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")


@router.message(Command("get"))
async def cmd_get(message: types.Message, command: CommandObject):
    try:
        args = command.args

        if args_validate(args):

            config_file = f"{CONFIG_DIR}/{args}.conf"
            if not os.path.exists(config_file):
                await message.reply(f"Файл конфигурации для клиента {args} не найден.")
                return

            file = FSInputFile(config_file)

            await message.reply_document(file, caption=f"Конфигурация для {args}")

        else:
            await message.reply("Пожалуйста, укажите имя конфига латиницей и без пробелов после команды /get.")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")
