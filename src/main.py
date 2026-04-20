import asyncio
import os
from pathlib import Path

import dotenv
from aiogram import Dispatcher

from routers.start_router import router as start_router
from src.core.telegram_bot import get_telegram_bot


async def main():
    dp = Dispatcher()
    dp.include_router(start_router)

    python_environment_file_path = Path(os.getcwd()) / ".env.python"
    dotenv.load_dotenv(python_environment_file_path)

    await dp.start_polling(get_telegram_bot())

if __name__ == "__main__":
    asyncio.run(main())