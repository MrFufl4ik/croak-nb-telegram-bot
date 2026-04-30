from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.data.bot_user import BotUser
from src.data.product_user import is_product_user_active
from src.dynamic.config import localisation_config, main_config

__start_menu_localisation: dict = localisation_config["start_menu"]
__support_config: dict = main_config["support"]

async def get_keyboard(bot_user: BotUser) -> InlineKeyboardMarkup:
    result = []

    status_menu_button = InlineKeyboardButton(
        text=__start_menu_localisation.get("status_menu_button", "Status"),
        callback_data="status_menu",
        style="primary"
    )
    offer_menu_button = InlineKeyboardButton(
        text=__start_menu_localisation.get("offer_menu_button", "Offer"),
        callback_data="offer_menu",
    )
    connect_menu_button = InlineKeyboardButton(
        text=__start_menu_localisation.get("connect_menu_button", "Connect"),
        callback_data="connect_menu",
        style="success"
    )
    inactive_connect_menu_button = InlineKeyboardButton(
        text=__start_menu_localisation.get("inactive_connect_menu_button", "Connect"),
        callback_data="inactive_connect_menu",
        style="danger"
    )
    support_menu_button = InlineKeyboardButton(
        text=__start_menu_localisation.get("support_menu_button", "Support"),
        url=__support_config.get("url", "https://google.com"),
    )
    admin_menu_button = InlineKeyboardButton(
        text=__start_menu_localisation.get("admin_menu_button", "Admin Panel"),
        callback_data="admin_menu",
    )


    is_exists = await is_product_user_active(bot_user)
    if is_exists: result.append([connect_menu_button])
    else: result.append([inactive_connect_menu_button])

    # Todo доработать поддержку
    result.append([status_menu_button])
    result.append([support_menu_button, offer_menu_button])

    if bot_user.is_admin: result.append([admin_menu_button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard