from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton

from src.core.telegram_bot import create_cancel_button
from src.dynamic.config import localisation_config

__connect_menu_localisation: dict = localisation_config["connect_menu"]

async def get_keyboard(connect_link: str) -> InlineKeyboardMarkup:
    result = []

    cancel_button = create_cancel_button("start_menu")

    result.append([cancel_button])

    # Todo добавить кнопку для перехода в Happ.

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard