from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatFullInfo

from src.core.telegram_bot import create_cancel_button
from src.data.bot_user import BotUser


async def get_keyboard(bot_user: BotUser) -> InlineKeyboardMarkup:
    result = []

    cancel_button = create_cancel_button("start_menu")
    result.append([cancel_button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard

async def get_userinfo_keyboard(chat_info: ChatFullInfo) -> InlineKeyboardMarkup:
    result = []

    go_to_account_button = InlineKeyboardButton(
        text="go to account",
        url=f"tg://user?id={chat_info.id}",
        style="success"
    )
    result.append([go_to_account_button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=result)
    return keyboard