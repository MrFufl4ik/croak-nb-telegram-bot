import os

from aiogram import Bot

bot: Bot | None = None

def get_telegram_bot() -> Bot:
    global bot
    if bot is not None: return bot
    bot = Bot(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
    return bot
