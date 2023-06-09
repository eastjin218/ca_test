import aioredis

class RedisConnection():
    def __init__(self):
        pass

    async def connect(self):
        redis = await aioredis.Redis.from_url(
            "redis://redis", max_connections=100, decode_responses=True
        )
        return redis