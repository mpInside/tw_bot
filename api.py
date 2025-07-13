from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from telegram_bot import bot, send_trading_signal
from logger import setup_logger

logger = setup_logger('api')

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

class Message(BaseModel):
    text: str

@app.post("/send-message")
async def send_message(message: Message):
    try:
        # Логируем входящее сообщение
        logger.info(f"Получено сообщение на API: {message.text}")
        
        result = await send_trading_signal(message.text)
        return result
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 