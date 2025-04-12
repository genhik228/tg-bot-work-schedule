import asyncio
from aiogram import Bot, Dispatcher
import logging

from config import TOKEN
from handlers import handlers

bot = Bot(TOKEN)

async def main():
    dp = Dispatcher()
    dp.include_routers(handlers.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())