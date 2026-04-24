import asyncio
import hashlib
import os
from datetime import timedelta
from pathlib import Path

from aiogram import Bot
from aiogram.types import Message, FSInputFile, InlineKeyboardButton

from redis import Redis
from src.core.redis.redis_clients import get_main_redis
from src.dynamic.config import main_config, localisation_config

bot: Bot | None = None

def get_telegram_bot() -> Bot:
    global bot
    if bot is not None: return bot
    bot = Bot(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
    return bot

__telegram_image_cache_config: dict = main_config["telegram_image_cache"]
__main_localisation: dict = localisation_config["main"]


def __sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

async def __async_sha256(data: bytes) -> str:
    return await asyncio.to_thread(__sha256, data)

async def get_cached_image(image_path: Path) -> str:
    redis: Redis = get_main_redis().redis

    image_bytes: bytes = open(image_path, 'rb').read()
    image_hash = await __async_sha256(image_bytes)

    redis_key = f"telegram_image_cache:{image_hash}"

    cached_file_id = await redis.get(redis_key)
    if cached_file_id:
        return cached_file_id.decode()

    user_for_cache = __telegram_image_cache_config.get("telegram_user_id", 1087240511)
    message: Message = await get_telegram_bot().send_photo(
        chat_id=user_for_cache,
        photo=FSInputFile(image_path)
    )
    file_id = message.photo[0].file_id
    await message.delete()

    expire_minutes: float = __telegram_image_cache_config.get("expire_minutes", 1.0)
    await redis.setex(redis_key, int(timedelta(minutes=expire_minutes).total_seconds()), file_id)
    return file_id

def create_cancel_button(callback_data: str) -> InlineKeyboardButton:
    result_button = InlineKeyboardButton(
        text=__main_localisation.get("cancel_button","Cancel"),
        callback_data=callback_data,
        style="danger"
    )
    return result_button