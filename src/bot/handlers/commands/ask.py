import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from services.ask import AskService

ask_router = Router()


class AskStates(StatesGroup):
    waiting_for_question = State()
    waiting_for_car_info = State()


@ask_router.message(Command("ask"))
async def cmd_ask(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, задайте ваш вопрос:")
    await state.set_state(AskStates.waiting_for_question)


@ask_router.message(AskStates.waiting_for_question)
async def process_question(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(
        "Теперь укажите информацию об автомобиле (марка, модель, год):"
    )
    await state.set_state(AskStates.waiting_for_car_info)


@ask_router.message(AskStates.waiting_for_car_info)
async def process_car_info(message: Message, state: FSMContext):
    await message.answer("⏳ Отправляю ваш запрос...")
    ask_service = AskService()
    data = await state.get_data()
    try:
        response = await ask_service.send(
            data={"question": data.get("question"), "car_info": message.text}
        )
        await message.answer(f"✅ Ответ от API:\n\n{response}")

    except Exception as e:
        logging.error(f"Не удалось подключиться к API: {e}")
        await message.answer(
            "❌ Произошла ошибка при обработке вашего запроса. Попробуйте позже."
        )

    await state.clear()
