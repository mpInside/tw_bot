# Telegram Message Forwarder Server

Сервер принимает POST-запросы с JSON данными и пересылает сообщения в указанный Telegram бот. Использует последние версии FastAPI и aiogram.

## Установка

1. Установите Python 3.8 или выше

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` с учетными данными вашего Telegram бота:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

Чтобы получить эти значения:
- Создайте нового бота через [@BotFather](https://t.me/botfather) в Telegram для получения токена бота
- Отправьте сообщение вашему боту и посетите `https://api.telegram.org/bot<YourBOTToken>/getUpdates` чтобы получить ваш chat ID

## Запуск сервера

Запустите сервер командой:
```bash
python server.py
```

Сервер будет доступен по адресу `http://localhost:8000`

## Использование

Отправьте POST-запрос на `http://localhost:8000/send-message` с JSON телом:
```json
{
    "text": "Ваше сообщение"
}
```

Пример использования curl:
```bash
curl -X POST http://185.87.193.73:8000/send-message \
     -H "Content-Type: application/json" \
     -d '{"text": "{{ticker}} OS 1h"}'
``` 
для cmd/

curl -X POST http://185.87.193.73:8000/send-message -H "Content-Type: application/json" -d "{\"text\": \"Symbol = 1000PEPEUSDT.P OS/OB signal  OS 1h\"}"
curl -X POST http://185.87.193.73:80/send-message -H "Content-Type: application/json" -d "{\"text\": \"Symbol = 1000PEPEUSDT.P OS/OB signal  OS 1h\"}"


мой комп
curl -X POST http://localhost:80/send-message -H "Content-Type: application/json" -d "{\"text\": \"Symbol = 1000PEPEUSDT.P OS/OB signal  OS 1h\"}"




