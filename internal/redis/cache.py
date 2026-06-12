import json
from functools import wraps

from internal.redis.redis import redis_client

def cache(ttl: int = 60):

    def decorator(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            cached_data = await redis_client.get(cache_key)

            if cached_data:
                return json.loads(cached_data)
            
            result = await func(*args, **kwargs)

            await redis_client.set(
                cache_key,
                json.dumps(result),
                ex=ttl
            )

            return result
        return wrapper
    return decorator