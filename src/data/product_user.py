from datetime import date

from sqlalchemy import Column, Integer, ForeignKey, exists, select, String, Date
from sqlalchemy.orm import Mapped, relationship

from src.core.database import database_clients
from src.core.database.database_base import Base
from src.data.bot_user import BotUser
from src.dynamic.config import main_config

database = database_clients.get_main_database()

__product_config: dict = main_config.get("product",{})
product_cost: int = __product_config.get("default_cost", 100)

class ProductUser(Base):
    __tablename__ = "product_user"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True, autoincrement=True)
    bot_user_id: Mapped[int] = Column(Integer, ForeignKey("bot_user.id"), unique=True)
    bot_user: Mapped[BotUser] = relationship("BotUser")
    cost: Mapped[int] = Column(Integer, default=product_cost, nullable=True)
    expires_at: Mapped[date] = Column(Date, nullable=False)
    connect_link: Mapped[str | None] = Column(String, nullable=True)

async def add_product_user(product_user: ProductUser):
    async with database.wrapper() as session:
        session.add(product_user)

async def is_product_user_exists(bot_user: BotUser) -> bool:
    async with database.wrapper() as session:
        subq = (
            select(ProductUser.id)
            .join(ProductUser.bot_user)
            .where(BotUser.telegram_id == bot_user.telegram_id)
        )
        stmt = select(exists(subq))
        result = await session.execute(stmt)
        return result.scalar()

async def get_product_user(bot_user: BotUser) -> ProductUser:
    async with database.wrapper() as session:
        stmt = select(ProductUser).join(ProductUser.bot_user).where(BotUser.telegram_id == bot_user.telegram_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def is_product_user_active(bot_user: BotUser) -> bool:
    is_exists = await is_product_user_exists(bot_user)
    if not is_exists: return False
    product_user = await get_product_user(bot_user)
    is_expired = product_user.expires_at <= date.today()
    if is_expired: return False
    return True