from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
import aiohttp
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, WEBHOOK_URL, SECRET_FINANDY
from logger import setup_logger

logger = setup_logger('telegram_bot')

# Initialize Telegram bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    try:
        # Extract ticker and side from callback data
        # Формат: "ticker|side"
        callback_data = callback_query.data
        if "|" in callback_data:
            ticker, side = callback_data.split("|", 1)
        
        # Проверяем наличие URL и секретного ключа
        if not WEBHOOK_URL:
            raise ValueError("WEBHOOK_URL не настроен")
        if not SECRET_FINANDY:
            raise ValueError("SECRET_FINANDY не настроен") 
        if not side:
            raise ValueError("Side не указан в callback_data")
        
        # Prepare the request data
        request_data = {
            "name": "1h OS/OB",
            "secret": SECRET_FINANDY,
            "symbol": ticker,
            "side": side
        }
        
        # Log request data
        logger.info(f"Отправляем запрос: URL: {WEBHOOK_URL}, Данные: {request_data}")
        
        # Send POST request to the other service
        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK_URL, json=request_data) as response:
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

async def send_trading_signal(symbol: str, signal_type: str, side: str):
    """
    Отправляет торговый сигнал в Telegram
    
    Параметры:
    - symbol: тикер торгового инструмента
    - signal_type: тип сигнала (например, "OS/OB signal")
    - side: сторона сделки ("buy" или "sell")
    """
    try:
        if not symbol:
            raise ValueError("Symbol is required")
        if not side:
            raise ValueError("Side is required")
        
        # Определяем эмодзи и текст для стороны сигнала
        if side.lower() == "buy":
            side_emoji = "🟢"
            side_text = "BUY"
            button_side_text = "Long"
        elif side.lower() == "sell":
            side_emoji = "🔴"
            side_text = "SELL"
            button_side_text = "Short"
        else:
            raise ValueError(f"Недопустимое значение side: {side}. Допустимые значения: 'buy' или 'sell'")
        
        # Create TradingView URL
        tradingview_url = f"https://www.tradingview.com/chart/?symbol={symbol}&interval=1H"
        
        # Create inline keyboard
        builder = InlineKeyboardBuilder()
        # Передаем и symbol, и side в callback_data через разделитель
        callback_data = f"{symbol}|{side}"
        # Текст кнопки зависит от стороны сделки
        button_text = f"🛒 Отправить заявку в {button_side_text}"
        builder.button(text=button_text, callback_data=callback_data)
        builder.adjust(1)  # Размещаем кнопки по одной в ряд
        
        # Создаем хэштег без ".P" на конце
        hashtag_symbol = symbol.rstrip(".P") if symbol.endswith(".P") else symbol
        
        # Format message with timestamp (символ как ссылка на TradingView)
        formatted_message = f"📨 Новое сообщение:\n<a href=\"{tradingview_url}\">{symbol}</a>\n{signal_type or 'OS/OB signal'}\n{side_emoji} {side_text}\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n#{hashtag_symbol}"
        
        # Send message to Telegram with inline keyboard
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=formatted_message,
            reply_markup=builder.as_markup(),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
            
        return {"status": "success", "message": "Message sent successfully"}
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {str(e)}")
        raise 