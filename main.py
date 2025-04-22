import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.start import start_router
from handlers.vin_number import vin_detector_router

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()


async def start():
    os.makedirs(name='photo', exist_ok=True)
    dp.include_router(start_router)
    dp.include_router(vin_detector_router)

    logging.basicConfig(level=logging.INFO)  # Чтобы видеть, как бот обрабатывает сообщения

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())
