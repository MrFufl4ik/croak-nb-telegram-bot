from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton

from src.core.telegram_bot import create_cancel_button
from src.dynamic.config import localisation_config, main_config

__prolong_menu_localisation: dict = localisation_config["prolong_menu"]
__prolong_config: dict = main_config["prolong"]

async def get_keyboard() -> InlineKeyboardMarkup:
    result = []

    cancel_button = create_cancel_button("start_menu")

    copy_bank_address_button = InlineKeyboardButton(
        text=__prolong_menu_localisation.get("copy_bank_address_button", "Copy bank address"),
        copy_text=CopyTextButton(text=__prolong_config.get("bank_address", "+09161234567")),
        style="success"
    )

    result.append([copy_bank_address_button])
    result.append([cancel_button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard