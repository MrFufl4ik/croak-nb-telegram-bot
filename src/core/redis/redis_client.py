from redis.asyncio import Redis

from src.core.redis.redis_config import RedisConnectConfig


class RedisClient:
    def __init__(self, redis_connect_config: RedisConnectConfig):
        self.redis = Redis(
            host="redis",
            port=redis_connect_config.port,
            db=redis_connect_config.logic_database,
            password=redis_connect_config.password
        )