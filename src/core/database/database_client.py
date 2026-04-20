from contextlib import asynccontextmanager
from sqlite3 import IntegrityError
from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.core.database.database_config import DatabaseConnectConfig

class DatabaseClient:
    def __init__(self, database_connect_config: DatabaseConnectConfig):
        self.engine = create_async_engine(
            f"postgresql+asyncpg://"
            f"{database_connect_config.user}:"
            f"{database_connect_config.password}@"
            f"database:"
            f"{database_connect_config.port}/"
            f"{database_connect_config.name}"
        )
        self.async_session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def wrapper(self):
        async with self.async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                raise RuntimeError("Database error") from e
            except Exception:
                await session.rollback()
                raise

    async def get_version(self) -> Optional[str]:
        async with self.engine.connect() as connection:
            result = await connection.execute(text("SELECT version()"))
            return result.scalar()