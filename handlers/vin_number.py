import os

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import Message
from dotenv import load_dotenv
from ai import ai

load_dotenv()
vin_detector_router = Router()

@vin_detector_router.message(F.content_type == ContentType.PHOTO)
async def vin_detector_handler(message: Message):
    """Распознавание VIN. Скачивание изображения, передача в сервис распознавания и получение распознанного VIN"""
    photo = message.photo[-1]

    file_id = photo.file_id
    file = await message.bot.get_file(file_id)
    img_url = f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/{file.file_path}"

    supposed_vin = await ai.recognize_vin(img_url)

    await message.answer(text=supposed_vin, parse_mode='Markdown')
    await message.answer(text='📋Рекомендуем перепроверить S и 5, E и B, 7 и L, если они встретились в VIN')

