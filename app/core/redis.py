from redis.asyncio import Redis

from app.core.config import settings

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True,
)
from redis.asyncio import Redis

from app.core.config import settings

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True,
)


async def clear_task_cache():
    keys = await redis_client.keys("tasks:*")

    if keys:
        await redis_client.delete(*keys)