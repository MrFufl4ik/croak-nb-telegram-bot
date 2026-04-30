from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.telegram_bot import create_cancel_button
from src.dynamic.config import localisation_config

__connect_menu_localisation: dict = localisation_config["connect_menu"]

async def get_keyboard() -> InlineKeyboardMarkup:
    result = []

    cancel_button = create_cancel_button("start_menu")

    main_connect_menu_button = InlineKeyboardButton(
        text=__connect_menu_localisation.get("main_connect_menu_button", "Connect [Main]"),
        callback_data="main_connect_menu",
        style="primary"
    )
    wl_connect_menu_button = InlineKeyboardButton(
        text=__connect_menu_localisation.get("wl_connect_menu_button", "Connect [WL]"),
        callback_data="wl_connect_menu",
        style="primary"
    )

    result.append([main_connect_menu_button])
    result.append([wl_connect_menu_button])
    result.append([cancel_button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard