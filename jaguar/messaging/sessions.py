from typing import List, Tuple

import aioredis
from nanohttp import settings


from ..redis_ import create_async_redis

_redis = None


def _get_member_key(member_id):
    return f'member:{member_id}'


async def redis():
    global _redis
    if _redis is None:
        _redis = await create_async_redis(settings.authentication.redis)
    return _redis


async def register_session(member_id, session_id, queue):
    await (await redis()).hset(
        _get_member_key(member_id),
        session_id,
        queue
    )


async def get_sessions(member_id: str) -> List[Tuple[str, str]]:
    session_queue = await (await redis()).hgetall(_get_member_key(member_id))
    for session, queue in session_queue.items():
        yield session, queue



async def cleanup_session(member_id: str, session_id: str):
    (await redis()).hdel(f'member:{member_id}', session_id)


async def flush_all():
    await (await redis()).flushdb()

