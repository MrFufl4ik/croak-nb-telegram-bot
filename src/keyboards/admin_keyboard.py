from aiogram.types import InlineKeyboardMarkup

from src.core.telegram_bot import create_cancel_button
from src.data.bot_user import BotUser


async def get_keyboard(bot_user: BotUser) -> InlineKeyboardMarkup:
    result = []

    cancel_button = create_cancel_button("start_menu")
    result.append([cancel_button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard