from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router(name="start router")


@start_router.message(CommandStart())
async def handle_start(message: Message) -> None:
    start_text = ("Добро пожаловать ! Пришлите фотографию с VIN номером и я распознаю её😎.\n\n"
                  ""
                  "Рекомендации:\n"
                  "- Фотография не размыта🤳\n"
                  "- Отклонение VIN номера на фотографии в пределах 30-40°\n")

    await message.answer(text=start_text)