from aiogram.types import InlineKeyboardMarkup

from src.core.telegram_bot import create_cancel_button


async def get_keyboard() -> InlineKeyboardMarkup:
    result = []

    cancel_button = create_cancel_button("start_menu")

    result.append([cancel_button])

    # Todo добавить кнопку для перехода в Happ.

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard