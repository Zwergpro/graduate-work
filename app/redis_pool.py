import redis

from flask import current_app


class _RedisPoolLazySingleton:
    _redis_pools = None

    def __new__(cls):
        if _RedisPoolLazySingleton._redis_pools is None:
            _RedisPoolLazySingleton._redis_pools = redis.ConnectionPool(
                host=current_app.config['REDIS_HOST'],
                port=current_app.config['REDIS_PORT'],
                password=current_app.config['REDIS_PASSWORD'],
                db=current_app.config['REDIS_DB'],
                decode_responses=True,
            )
        return _RedisPoolLazySingleton._redis_pools


def redis_connection(strict=False):
    pool = _RedisPoolLazySingleton()
    if strict:
        return redis.StrictRedis(connection_pool=pool)
    else:
        return redis.Redis(connection_pool=pool)
