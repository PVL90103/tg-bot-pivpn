# Telegram Bot Pivpn

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

`nano /etc/systemd/system/telegram_bot.service`

Создать файл сервиса. Нужно указать директорию с проектом {PROJECT_DIR}.
```
cat > /etc/systemd/system/telegram_bot.service <<EOL
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
User=root
WorkingDirectory={PROJECT_DIR}
ExecStart=/usr/bin/make run
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL
```
- `systemctl daemon-reload` Перезагружаем systemd
- `systemctl enable telegram_bot.service` Включаем и запускаем сервис
- `systemctl start telegram_bot.service`
- `systemctl status telegram_bot.service` Проверяем статус сервиса

## Usage

Commands:  
- `/clients` - вывод всех клиентов  
- `/add <name>` - добавление нового клиента  
- `/remove <name>` - полное удаление конфигов клиента  
- `/off <name>` - отключение клиента, без удаления конфигов  
- `/on <name>` - включение клиента  
- `/qr <name>` - Получение QR кода для подключения клиента  
- `/get <name>` - Получение конфиг файла для подключения клиента
