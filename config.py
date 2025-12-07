import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Trading configuration
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
SECRET_FINANDY = os.getenv('SECRET_FINANDY')

# Server configuration
HOST = "0.0.0.0"
PORT = 80

# Проверка обязательных переменных окружения
required_vars = {
    'TELEGRAM_BOT_TOKEN': TELEGRAM_BOT_TOKEN,
    'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
    'WEBHOOK_URL': WEBHOOK_URL,
    'SECRET_FINANDY': SECRET_FINANDY
}

missing_vars = [var for var, value in required_vars.items() if value is None]
if missing_vars:
    raise ValueError(f"Отсутствуют обязательные переменные окружения: {', '.join(missing_vars)}") 