from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "👋 Добро пожаловать!\n\n"
        "Я бот для обработки вопросов об автомобилях.\n\n"
        "Доступные команды:\n"
        "/start - показать это сообщение\n"
        "/ask - задать вопрос о автомобиле\n"
        "/parse - получить информацию о машине по url объявления\n\n"
        "Просто нажмите /ask чтобы начать!"
    )
    await message.answer(welcome_text)
