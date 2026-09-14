from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis, ConnectionPool

from core.config import settings

pool = ConnectionPool.from_url(settings.redis_url)

async def get_redis():
    """Get Redis client."""
    async with Redis(connection_pool=pool) as client:
        yield client

RedisDep = Annotated[Redis, Depends(get_redis)]
