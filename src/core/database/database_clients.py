from typing import Optional

from src.core.database.database_client import DatabaseClient
from src.core.database.database_config import DatabaseConnectConfig

from src.dynamic.config import database_config

__main_database_instance: Optional[DatabaseClient] = None

def get_main_database() -> DatabaseClient:
    global __main_database_instance
    if __main_database_instance is None:
        main_database_config: DatabaseConnectConfig = DatabaseConnectConfig.from_dict(database_config)
        __main_database_instance = DatabaseClient(main_database_config)
    return __main_database_instance