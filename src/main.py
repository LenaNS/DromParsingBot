import asyncio

from aiogram import Bot, Dispatcher

from bot.handlers.router import router
from settings import Settings


async def main():
    config = Settings.load()

    dp = Dispatcher()
    dp.include_router(router=router)

    bot = Bot(token=config.token.get_secret_value())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
