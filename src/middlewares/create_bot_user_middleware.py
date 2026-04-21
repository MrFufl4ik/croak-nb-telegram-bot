from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.data.bot_user import BotUser, add_bot_user, is_bot_user_exists_by_telegram_id


class CreateBotUserMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: dict[str, Any]) -> Any:
        user: user = data.get("event_from_user")
        if not user or not user.id: return await handler(event, data)
        bot_user_exists = await is_bot_user_exists_by_telegram_id(user.id)
        if not bot_user_exists:
            bot_user = BotUser(telegram_id=user.id)
            await add_bot_user(bot_user)
        return await handler(event, data)