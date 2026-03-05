import logging
import asyncio
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
from handlers import start, services, order, support

load_dotenv()

async def main():
    bot = Bot(os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(services.router)
    dp.include_router(order.router)
    dp.include_router(support.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())