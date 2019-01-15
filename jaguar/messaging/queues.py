import asyncio
from typing import Callable

import ujson
import redis
import aioredis
from nanohttp import settings


_blocking_redis = None
_async_redis = None


def create_blocking_redis():
    return redis.StrictRedis(**settings.messaging.redis)


async def create_async_redis():
    params = settings.messaging.redis
    return await aioredis.create_redis(
        (params.host, params.port),
        db=params.db,
        password=params.password,
        loop=asyncio.get_event_loop()
    )


def blocking_redis():
    global _blocking_redis
    if _blocking_redis is None:
        _blocking_redis = create_blocking_redis()

    return _blocking_redis


async def async_redis():
    global _async_redis
    if _async_redis is None:
        _async_redis = await create_async_redis()

    return _async_redis


def push(queue, message):
    blocking_redis().lpush(queue, ujson.dumps(message))


async def push_async(queue: str, message: str):
    await (await async_redis()).lpush(queue, ujson.dumps(message))


async def pop_async(queue):
    encoded_message = await (await async_redis()).rpop(queue)
    return ujson.loads(encoded_message) if encoded_message else None


