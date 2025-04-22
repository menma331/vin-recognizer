import os

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.types import Message
from dotenv import load_dotenv
from ai import ai
from utils import determine_image_rotation, rotate_image

load_dotenv()
vin_detector_router = Router()

@vin_detector_router.message(F.content_type == ContentType.PHOTO)
async def vin_detector_handler(message: Message):
    """Распознавание VIN. Скачивание изображения, передача в сервис распознавания и получение распознанного VIN"""
    photo = message.photo[-1]

    file_id = photo.file_id
    file = await message.bot.get_file(file_id)
    img_url = f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/{file.file_path}"

    file_name = f"photo/{photo.file_unique_id}.jpg"
    await message.bot.download(file=photo.file_id, destination=file_name)

    rotate_to = determine_image_rotation(image_path=file_name)
    processed_image = rotate_image(image_path=file_name, output_path=f"{file_name}_output", rotate=rotate_to)
    supposed_vin = await ai.recognize_vin(processed_image)

    await message.answer(text=supposed_vin, parse_mode='Markdown')
    await message.answer(text='📋Рекомендуем перепроверить S и 5, E и B, 7 и L, если они встретились в VIN')

    os.remove(processed_image)
    os.remove(file_name)

