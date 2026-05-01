from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CopyTextButton

from src.core.telegram_bot import create_cancel_button
from src.data.bot_user import BotUser
from src.data.product_user import get_final_cost_by_bot_user
from src.dynamic.config import localisation_config, main_config

__prolong_menu_localisation: dict = localisation_config["prolong_menu"]
__prolong_config: dict = main_config["prolong"]
__product_config: dict = main_config["product"]

async def get_keyboard(bot_user: BotUser) -> InlineKeyboardMarkup:
    result = []

    cancel_button = create_cancel_button("start_menu")

    price_caption = __prolong_menu_localisation.get("price_button", "{0} / {1}")
    cost = await get_final_cost_by_bot_user(bot_user)
    price_caption = price_caption.format(
        cost,
        __product_config.get("subscription_day_count", 30)
    )
    price_button = InlineKeyboardButton(
        text=price_caption,
        callback_data="price_button_click",
        style="primary"
    )
    copy_bank_address_button = InlineKeyboardButton(
        text=__prolong_menu_localisation.get("copy_bank_address_button", "Copy bank address"),
        copy_text=CopyTextButton(text=__prolong_config.get("bank_address", "+09161234567")),
        style="success"
    )

    result.append([price_button])
    result.append([copy_bank_address_button])
    result.append([cancel_button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard