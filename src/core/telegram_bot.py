import os
from datetime import timedelta
from pathlib import Path

from aiogram import Bot
from aiogram.types import Message, FSInputFile

from redis import Redis
from src.core.redis.redis_clients import get_main_redis
from src.dynamic.config import main_config

bot: Bot | None = None

def get_telegram_bot() -> Bot:
    global bot
    if bot is not None: return bot
    bot = Bot(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
    return bot

__telegram_image_cache_config: dict = main_config["telegram_image_cache"]
async def get_cached_image(image_path: Path) -> str:
    redis: Redis = get_main_redis().redis
    redis_key = f"telegram_image_cache:{image_path}"

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