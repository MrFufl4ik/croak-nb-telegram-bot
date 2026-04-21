from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.data.bot_user import get_bot_user_by_telegram_id


class VerifyBotUserMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: dict[str, Any]) -> Any:
        user: user = data.get("event_from_user")
        if not user or not user.id: return await handler(event, data)
        bot_user = await get_bot_user_by_telegram_id(user.id)
        if not bot_user.is_verified: return None
        return await handler(event, data)