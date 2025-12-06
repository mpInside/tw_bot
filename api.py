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

class TradingViewSignal(BaseModel):
    Type: str
    Symbol: str
    GoLong: int
    GoShort: int

@app.post("/tradingview-signal")
async def tradingview_signal(signal: TradingViewSignal):
    try:
        # Логируем входящий сигнал
        logger.info(f"Получен сигнал от TradingView: Type={signal.Type}, Symbol={signal.Symbol}, GoLong={signal.GoLong}, GoShort={signal.GoShort}")
        
        # Проверка: оба флага не могут быть равны 0 одновременно
        if signal.GoLong == 0 and signal.GoShort == 0:
            raise ValueError("Оба флага GoLong и GoShort не могут быть равны 0 одновременно")
        
        # Проверка: оба флага не могут быть равны 1 одновременно
        if signal.GoLong == 1 and signal.GoShort == 1:
            raise ValueError("Оба флага GoLong и GoShort не могут быть равны 1 одновременно")
        
        # Определяем сторону сигнала
        if signal.GoLong == 1:
            side = "buy"
        elif signal.GoShort == 1:
            side = "sell"
        
        result = await send_trading_signal(
            symbol=signal.Symbol,
            signal_type=signal.Type,
            side=side
        )
        return result
    except Exception as e:
        logger.error(f"Ошибка при обработке сигнала: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 