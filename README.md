# Telegram Bot Pivpn

Итоговый проект по курсу "Python для инженеров" 2024

Бот для управления WireGuard туннелями на сервере через утилиту PiVPN

## Technologies
- Python3.12
- Aiogram 3
- WireGuard
- PiVPN

## Requirements
 - Ubuntu server >=20.04
 - Installed PiVPN https://github.com/pivpn/pivpn

## Installation
1. Запустить скрипт для установки Python3.12
    
```
chmod +x scripts/install-python3.12.sh
scripts/install-python3.12.sh
```

2. Создать файл .env. Указать в нем переменные
```
BOT_TOKEN= #Токен телеграм бота
ADMIN_IDS= #ID администраторов, те кто сможет выполнять команды
CONFIG_DIR= #Путь до директории с конфигами WG (/etc/wireguard/configs)
```
3. Запустить сборку через make
```
make start
```
4. Создать сервис в systemd

## Usage

Commands:  
- `/clients` - вывод всех клиентов  
- `/add <name>` - добавление нового клиента  
- `/remove <name>` - полное удаление конфигов клиента  
- `/off <name>` - отключение клиента, без удаления конфигов  
- `/on <name>` - включение клиента  
- `/qr <name>` - Получение QR кода для подключения клиента  
- `/get <name>` - Получение конфиг файла для подключения клиента
