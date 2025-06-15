import asyncio
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message


class TimeoutMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        try:
            await asyncio.wait_for(handler(event, data), timeout=5.0)
        except TimeoutError:
            await event.answer("Время ожидания ответа истекло")
            state = data.get("state")
            if state:
                await state.finish()
