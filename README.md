# Telegram Trading Bot Server

Сервер принимает POST-запросы с торговыми сигналами и пересылает их в Telegram бот с интерактивными кнопками для открытия в TradingView и отправки торговых заявок. Использует FastAPI, aiogram и асинхронную архитектуру.

## Возможности

- 📨 Прием торговых сигналов через REST API
- 🤖 Автоматическая отправка в Telegram с форматированием
- 📈 Кнопка для открытия графика в TradingView
- 🛒 Кнопка для отправки торговой заявки
- 📝 Подробное логирование всех операций
- ⏰ Автоматическое добавление временных меток

## Архитектура

- **main.py** - Точка входа, запуск сервера и бота
- **api.py** - FastAPI сервер с эндпоинтом `/send-message`
- **telegram_bot.py** - Логика Telegram бота и обработка сигналов
- **config.py** - Конфигурация и переменные окружения
- **logger.py** - Система логирования
- **tradingview.py** - Интеграция с TradingView (если используется)

## Установка

1. Установите Python 3.8 или выше

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` с необходимыми переменными окружения:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
WEBHOOK_URL_BUY=your_webhook_url_here
SECRET_FINANDY_BUY=your_secret_key_here
```

### Получение учетных данных

- **TELEGRAM_BOT_TOKEN**: Создайте бота через [@BotFather](https://t.me/botfather) в Telegram
- **TELEGRAM_CHAT_ID**: Отправьте сообщение боту и посетите `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
- **WEBHOOK_URL_BUY**: URL для отправки торговых заявок
- **SECRET_FINANDY_BUY**: Секретный ключ для аутентификации

## Запуск сервера

Запустите сервер командой:
```bash
python main.py
```

Сервер будет доступен по адресу `http://localhost:80`

## API Endpoints

### POST /send-message

Отправляет торговый сигнал в Telegram.

**Тело запроса:**
```json
{
    "text": "Symbol = 1000PEPEUSDT.P OS/OB signal  OS 1h"
}
```

**Ответ:**
```json
{
    "status": "success",
    "message": "Message sent successfully"
}
```

## Логирование

Все операции логируются в папку `logs/` с разделением по модулям:
- `main_YYYYMMDD.log` - логи основного процесса
- `api_YYYYMMDD.log` - логи API запросов
- `telegram_bot_YYYYMMDD.log` - логи Telegram бота

## Структура проекта

```
tw_bot/
├── main.py              # Точка входа
├── api.py               # FastAPI сервер
├── telegram_bot.py      # Telegram бот
├── config.py            # Конфигурация
├── logger.py            # Логирование
├── tradingview.py       # TradingView интеграция
├── requirements.txt     # Зависимости
├── .env                 # Переменные окружения
└── logs/                # Лог файлы
```

## Примеры использования

### Для cmd/
```bash
curl -X POST http://185.87.193.73:80/send-message -H "Content-Type: application/json" -d "{\"text\": \"Symbol = 1000PEPEUSDT.P OS/OB signal  OS 1h\"}"
```

### Для local
```bash
curl -X POST http://localhost:80/send-message -H "Content-Type: application/json" -d "{\"text\": \"Symbol = 1000PEPEUSDT.P OS/OB signal  OS 1h\"}"
``` 




