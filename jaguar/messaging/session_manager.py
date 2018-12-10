import asyncio
from typing import List, Callable, Tuple
from os import path

import aio_pika
import aiohttp
import aioredis
import itsdangerous
from aiohttp import web
from nanohttp import settings
from restfulpy.configuration import configure as restfulpy_configure
from restfulpy.principal import JwtPrincipal
from restfulpy.orm import DBSession
from aio_pika.channel import Channel as RabbitChannel

from jaguar import Jaguar
from ..models import TargetMember, Member


class SessionManager:
    _redis = None

    @classmethod
    async def redis(cls):
       if cls._redis is None:
           cls._redis = await aioredis.create_redis(
               f'redis://{settings.authentication.redis.host}:' \
               f'{settings.authentication.redis.port}',
               db=settings.authentication.redis.db,
            )
       return cls._redis

    async def register_session(self, member_id, session_id, queue):
        self._redis.hset(
            f'member:{member_id}',
            session_id,
            queue
        )

    async def get_sessions(self, member_id: str) -> List[Tuple[str, str]]:
        session_queue = await self._redis.hgetall(f'member:{member_id}')
        active_sessions = [
            (session, queue) for session, queue in session_queue.items()
        ]

        return active_sessions or None

    async def cleanup_session(self, member_id: str, session_id: str):
        self._redis.hdel(f'member:{member_id}', session_id)

