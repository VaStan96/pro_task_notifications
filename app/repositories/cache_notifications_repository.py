from db.redis import get_redis

async def get_data(key: str):
    redis = await get_redis()
    if redis:
        return await redis.get(key)
    else:
        return None

async def set_data(key: str, value: str):
    redis = await get_redis()
    if redis:
        await redis.set(key, value, ex=3600)

async def del_data(key: str):
    redis = await get_redis()
    if redis:
        await redis.delete(key)