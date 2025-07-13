import asyncio
import os
import nest_asyncio
import uvicorn
from telegram_bot import dp, bot
from api import app
from logger import setup_logger

logger = setup_logger('main')

if __name__ == "__main__":
    # Enable nested event loops
    nest_asyncio.apply()
    
    # Set event loop policy for Windows
    if os.name == 'nt':  # Windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Create event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Start the bot polling in the background
    polling_task = loop.create_task(dp.start_polling(bot))
    
    # Start the FastAPI server
    config = uvicorn.Config(app, host="0.0.0.0", port=80, loop=loop)
    server = uvicorn.Server(config)
    
    
    async def shutdown():
        logger.info("Shutting down...")
        # Stop the bot polling
        await dp.stop_polling()
        # Close the bot session
        await bot.session.close()
        # Stop the server
        await server.shutdown()
    
    try:
        # Start the server
        logger.info("Server started.")
        loop.run_until_complete(server.serve())
    except KeyboardInterrupt:
        loop.run_until_complete(shutdown())
    finally:
        loop.close()
        logger.info("Server stopped.") 