import asyncio
import logging
import os
from pathlib import Path

import dotenv
from aiogram import Dispatcher

from routers.start_router import router as start_router
from routers.status_router import router as status_router
from routers.prolong_router import router as prolong_router
from routers.connect_router import router as connect_router
from routers.main_connect_router import router as main_connect_router
from routers.wl_connect_router import router as wl_connect_router
from routers.offer_router import router as offer_router
from routers.admin_router import router as admin_router
from src.core.database.database_base import Base
from src.core.database.database_clients import get_main_database
from src.core.telegram_bot import get_telegram_bot
from src.middlewares.create_bot_user_middleware import CreateBotUserMiddleware
from src.middlewares.verify_bot_user_middleware import VerifyBotUserMiddleware


async def init_database() -> None:
    database = get_main_database()
    async with database.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger = logging.getLogger(__name__)
    logger.info(await database.get_version())


def init_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )

def init_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    #middlewares
    dp.update.middleware(CreateBotUserMiddleware())
    dp.update.middleware(VerifyBotUserMiddleware())
    #routers
    dp.include_router(start_router)
    dp.include_router(connect_router)
    dp.include_router(prolong_router)
    dp.include_router(main_connect_router)
    dp.include_router(wl_connect_router)
    dp.include_router(status_router)
    dp.include_router(offer_router)
    dp.include_router(admin_router)
    return dp

def init_environment_variables() -> None:
    python_environment_file_path = Path(os.getcwd()) / ".env.python"
    dotenv.load_dotenv(python_environment_file_path)

async def main():
    init_logging()
    await init_database()
    init_environment_variables()
    dp = init_dispatcher()
    await dp.start_polling(get_telegram_bot())

if __name__ == "__main__":
    asyncio.run(main())