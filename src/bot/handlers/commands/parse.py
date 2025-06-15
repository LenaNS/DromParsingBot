import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from services.parse import DromService

parse_router = Router()


class ParseStates(StatesGroup):
    waiting_for_url = State()


@parse_router.message(Command("parse"))
async def cmd_parse(message: Message, state: FSMContext):
    await message.answer("Укажите url адрес страницы объявления:")
    await state.set_state(ParseStates.waiting_for_url)


@parse_router.message(ParseStates.waiting_for_url)
async def process_url(message: Message, state: FSMContext):
    url = message.text
    parser = DromService()
    await message.answer("⏳ Запрос отправлен...")
    try:
        data = await parser.parse(url)
        msg = "\n".join(f"{k}: {v}" for k, v in data.items())
        await message.answer(msg)
    except Exception as e:
        logging.error(f"Не удалось найти страницу: {e}")
        await message.answer("Не удалось найти страницу.")

    await state.clear()
