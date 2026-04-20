from sqlalchemy import Column, Integer, Boolean, exists, select
from sqlalchemy.orm import Mapped

from src.core.database import database_clients
from src.core.database.database_base import Base

database = database_clients.get_main_database()

class BotUser(Base):
    __tablename__ = "bot_user"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id: Mapped[int] = Column(Integer, unique=True)
    is_verified: Mapped[bool] = Column(Boolean, default=False)
    is_admin: Mapped[bool] = Column(Boolean, default=False)

async def add_bot_user(bot_user: BotUser):
    async with database.wrapper() as session:
        session.add(bot_user)

async def is_bot_user_exist_with_telegram_id(telegram_id: int) -> bool:
    async with database.wrapper() as session:
        stmt = select(exists().where(BotUser.telegram_id == telegram_id))
        result = await session.execute(stmt)
        return result.scalar()