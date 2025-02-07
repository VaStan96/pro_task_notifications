from redis.asyncio import Redis
import config

redis: Redis | None = None

async def get_redis() -> Redis:
    global redis
    if redis is None:
        redis = await Redis.from_url(config.REDIS_URL, encoding="utf-8", decode_responses=True)
    return redis


async def close_redis():
    global redis
    if redis:
        await redis.close()