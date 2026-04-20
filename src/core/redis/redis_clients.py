from typing import Optional

from redis.asyncio import Redis

from src.core.redis.redis_client import RedisClient
from src.core.redis.redis_config import RedisConnectConfig
from src.dynamic.config import redis_config

__main_redis_instance: Redis | None = None

def get_main_redis() -> RedisClient:
    global __main_redis_instance
    if __main_redis_instance is None:
        main_redis_config: RedisConnectConfig = RedisConnectConfig.from_dict(redis_config)
        __main_redis_instance = RedisClient(main_redis_config)
    return __main_redis_instance