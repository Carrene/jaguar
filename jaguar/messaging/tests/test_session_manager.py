import asyncio

import aioredis
from nanohttp import settings
from restfulpy.principal import JwtPrincipal

from jaguar.models import Member
from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.messaging.websocket import SessionManager


class TestWebsocketConnection(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        cls.redis_attrs = dict(
            host=settings.authentication.redis.host,
            port=settings.authentication.redis.port,
            password=settings.authentication.redis.password,
            db=15
        )
        session = cls.create_session()
        member = Member(
            email='member@example.com',
            title='member',
            access_token='access token',
            reference_id=1
        )
        session.add(member)
        session.commit()

    async def test_register(self, websocket_session):
        self.login('member@example.com')

        loop = asyncio.get_event_loop()

        redis = await aioredis.create_redis(
            f'redis://{self.redis_attrs["host"]}:{self.redis_attrs["port"]}',
            db=self.redis_attrs['db'],
            loop=loop
        )
        await redis.flushdb()

        token = JwtPrincipal.load(self._authentication_token)
        session_manager = SessionManager(redis)

        async with websocket_session(token=self._authentication_token) as ws:

            await session_manager.register_session(
                member=token.id,
                session=token.session_id,
                queue='queue'
            )

            active_sessions = await session_manager.get_session(member=token.id)
            assert active_sessions[0] == (token.id, token.session_id)

            await redis.flushdb()

            active_sessions = await session_manager.get_session(member=token.id)
            assert active_sessions[0] == None

            assert 1 == 1

