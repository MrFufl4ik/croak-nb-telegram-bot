from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.dynamic.config import localisation_config

__start_menu_localisation: dict = localisation_config["start_menu"]

def get_keyboard() -> InlineKeyboardMarkup:
    result = []

    status_menu_button = InlineKeyboardButton(
        text=__start_menu_localisation.get("status_menu_button", ""),
        callback_data="status_menu"
    )

    result.append([status_menu_button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard