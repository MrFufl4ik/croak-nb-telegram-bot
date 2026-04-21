from sqlalchemy import Column, Integer, DateTime, ForeignKey, exists, select
from sqlalchemy.orm import Mapped

from src.core.database import database_clients
from src.core.database.database_base import Base
from src.dynamic.config import main_config

database = database_clients.get_main_database()

__product_config: dict = main_config.get("product",{})
product_cost: int = __product_config.get("cost", 200)

class ProductUser(Base):
    __tablename__ = "product_user"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bot_user_id: Mapped[int] = Column(Integer, ForeignKey("bot_user.id"), unique=True)
    cost: Mapped[int] = Column(Integer, default=product_cost, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

async def is_product_user_exists_by_telegram_id(telegram_id: int) -> bool:
    async with database.wrapper() as session:
        stmt = select(exists().where(ProductUser.bot_user_id == telegram_id))
        result = await session.execute(stmt)
        return result.scalar()

async def get_product_user_by_telegram_id(telegram_id: int) -> ProductUser:
    async with database.wrapper() as session:
        stmt = select(ProductUser).where(ProductUser.bot_user_id == telegram_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()