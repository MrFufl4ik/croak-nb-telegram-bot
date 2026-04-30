from datetime import datetime
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.data.bot_user import BotUser, add_bot_user, is_bot_user_exists_by_telegram_id, get_bot_user_by_telegram_id
from src.data.product_user import is_product_user_exists, ProductUser, add_product_user


class CreateBotUserMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: dict[str, Any]) -> Any:
        user: user = data.get("event_from_user")
        if not user or not user.id: return await handler(event, data)
        bot_user_exists = await is_bot_user_exists_by_telegram_id(user.id)
        if not bot_user_exists:
            bot_user = BotUser(telegram_id=user.id)
            await add_bot_user(bot_user)
        bot_user = await get_bot_user_by_telegram_id(user.id)
        product_user_exists = await is_product_user_exists(bot_user)
        if not product_user_exists:
            product_user = ProductUser(bot_user_id=bot_user.id, expires_at=datetime(1970, 1, 1))
            await add_product_user(product_user)
        return await handler(event, data)