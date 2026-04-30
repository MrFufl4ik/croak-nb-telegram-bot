from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton

from src.core.telegram_bot import create_cancel_button
from src.dynamic.config import localisation_config

async def get_keyboard() -> InlineKeyboardMarkup:
    result = []

    cancel_button = create_cancel_button("connect_menu")

    result.append([cancel_button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard