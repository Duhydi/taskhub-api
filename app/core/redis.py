from redis.asyncio import Redis

from app.core.config import settings

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    decode_responses=True,
)


async def clear_task_cache(
    project_id: int | None = None,
) -> None:
    if project_id is None:
        pattern = "project:*:tasks:*"
    else:
        pattern = f"project:{project_id}:tasks:*"

    keys = []

    async for key in redis_client.scan_iter(
        match=pattern,
    ):
        keys.append(key)

    if keys:
        await redis_client.delete(*keys)