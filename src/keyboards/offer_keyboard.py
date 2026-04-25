from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.telegram_bot import create_cancel_button
from src.dynamic.config import localisation_config, main_config

__offer_config: dict = main_config["offer"]
__offer_menu_localisation: dict = localisation_config["offer_menu"]

async def get_keyboard() -> InlineKeyboardMarkup:
    result = []

    cancel_button = create_cancel_button("start_menu")
    read_button = InlineKeyboardButton(
        text=__offer_menu_localisation.get("read_button", "Read"),
        url=__offer_config.get("url", "https://google.ocm"),
        style="success"
    )

    result.append([read_button])
    result.append([cancel_button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard