import pytest
import aiohttp
import aioredis
from nanohttp import settings
from restfulpy.principal import JwtPrincipal
from bddrest.authoring import when, Update, Remove, status

from jaguar.models import Member
from jaguar.messaging.sessions import SessionManager
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestWebsocketConnection(AutoDocumentationBDDTest):

    async def setup(self):
        self.redis = await aioredis.create_redis(
            f'redis://{settings.authentication.redis.host}:' \
            f'{settings.authentication.redis.port}',
            db=settings.authentication.redis.db,
        )
        await self.redis.flushdb()

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        member = Member(
            email='member@example.com',
            title='member',
            access_token='access token',
            reference_id=1
        )
        contact1 = Member(
            email='contact1@example.com',
            title='contact1',
            access_token='access token',
            reference_id=2
        )
        member.contacts.append(contact1)
        session.add(member)
        session.commit()


    async def test_websocket(self, websocket_session):
        self.login('member@example.com')
        await self.setup()

        with pytest.raises(aiohttp.WSServerHandshakeError):
            async with websocket_session() as ws:
               pass

        session_manager = SessionManager()

        async with websocket_session(token=self._authentication_token) as ws:
            token = JwtPrincipal.load(self._authentication_token)

            registered_session = await self.redis.hget(
                f'member:{token.id}',
                token.session_id
            )

            assert registered_session == settings.rabbitmq.websocket_queue.encode()

            active_sessions = await session_manager.get_sessions(token.id)

            assert 1 == 1
            assert active_sessions[0] == (
                token.session_id.encode(),
                settings.rabbitmq.websocket_queue.encode()
            )

        await ws.send_str('close')

        active_sessions = await session_manager.get_sessions(token.id)
        assert len(active_sessions) == 0

        await self.redis.flushdb()

