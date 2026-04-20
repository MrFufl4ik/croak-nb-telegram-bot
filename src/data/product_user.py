from sqlalchemy import Column, Integer, DateTime
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
    cost: Mapped[int] = Column(Integer, default=product_cost, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)