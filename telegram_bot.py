from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
import aiohttp
import re
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, WEBHOOK_URL_BUY, SECRET_FINANDY_BUY
from logger import setup_logger

logger = setup_logger('telegram_bot')

# Initialize Telegram bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    try:
        # Extract ticker from callback data
        ticker = callback_query.data
        
        # Проверяем наличие URL и секретного ключа
        if not WEBHOOK_URL_BUY:
            raise ValueError("WEBHOOK_URL_BUY не настроен")
        if not SECRET_FINANDY_BUY:
            raise ValueError("SECRET_FINANDY_BUY не настроен")
        
        # Prepare the request data
        request_data = {
            "name": "Buy OS",
            "secret": SECRET_FINANDY_BUY,
            "symbol": ticker,
            "side": "buy"
        }
        
        # Log request data
        logger.info(f"Отправляем запрос: URL: {WEBHOOK_URL_BUY}, Данные: {request_data}")
        
        # Send POST request to the other service
        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK_URL_BUY, json=request_data) as response:
                # Get response data
                response_data = await response.text()
                logger.info(f"Ответ сервера: Статус: {response.status}, Тело ответа: {response_data}")
                
                if response.status == 200:
                    await callback_query.answer("Заявка успешно отправлена!")
                else:
                    await callback_query.answer("Ошибка при отправке заявки", show_alert=True)
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        await callback_query.answer(f"Произошла ошибка: {str(e)}", show_alert=True)

async def send_trading_signal(message_text: str):
    """
    Отправляет торговый сигнал в Telegram
    """
    try:
        # Извлекаем тикер из сообщения
        ticker_match = re.search(r'Symbol = (.*?) OS/OB signal', message_text)
        if not ticker_match:
            raise ValueError("No ticker found in message")
        
        # Извлекаем тикер из первой группы совпадения регулярного выражения
        ticker = ticker_match.group(1)
        
        # Create TradingView URL
        tradingview_url = f"https://www.tradingview.com/chart/?symbol={ticker}&interval=1H"
        
        # Create inline keyboard
        builder = InlineKeyboardBuilder()
        builder.button(text="📈 Открыть в TradingView", url=tradingview_url)
        builder.button(text="🛒 Отправить заявку", callback_data=ticker)
        builder.adjust(1)  # Размещаем кнопки по одной в ряд
        
        # Format message with timestamp
        formatted_message = f"📨 Новое сообщение:\n\n{ticker}\n\nOS/OB signal\n\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        
        # Send message to Telegram with inline keyboard
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=formatted_message,
            reply_markup=builder.as_markup()
        )
            
        return {"status": "success", "message": "Message sent successfully"}
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {str(e)}")
        raise 