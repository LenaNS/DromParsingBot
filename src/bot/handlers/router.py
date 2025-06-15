from aiogram import Router

from bot.handlers.commands.ask import ask_router
from bot.handlers.commands.parse import parse_router
from bot.handlers.commands.start import start_router

router = Router()

router.include_router(start_router)
router.include_router(ask_router)
router.include_router(parse_router)
