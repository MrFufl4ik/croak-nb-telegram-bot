from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.data.bot_user import BotUser
from src.data.product_user import is_product_user_active
from src.dynamic.config import localisation_config

__start_menu_localisation: dict = localisation_config["start_menu"]

async def get_keyboard(bot_user: BotUser) -> InlineKeyboardMarkup:
    result = []

    status_menu_button = InlineKeyboardButton(
        text=__start_menu_localisation.get("status_menu_button", "Status"),
        callback_data="status_menu"
    )
    connect_menu_button = InlineKeyboardButton(
        text=__start_menu_localisation.get("connect_menu_button", "Connect"),
        callback_data="connect_menu"
    )

    is_exists = await is_product_user_active(bot_user)
    if is_exists: result.append([connect_menu_button])
    result.append([status_menu_button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard