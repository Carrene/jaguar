import redis
import aioredis
import aiohttp
import pytest
from nanohttp import settings

from jaguar.models import Member
from jaguar.messaging.websocket import SessionManager
from jaguar.tests.helpers import AutoDocumentationBDDTest


class TestWebsocketConnection(AutoDocumentationBDDTest):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.redis = aioredis.create_redis(
            f'redis://{settings.authentication.redis.host}:' \
            f'{settings.authentication.redis.port}',
            db=settings.authentication.redis.db,
        )

    async def setup(self):
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
        self.setup()

        session_manager = SessionManager()

        with pytest.raises(aiohttp.WSServerHandshakeError):
            async with websocket_session() as ws:
               pass

        async with websocket_session(token=self._authentication_token) as ws:
            await ws.send_str('close')
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print('Server: ', msg.data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break

            assert self.redis.hget(token.id, token.session_id) is not None

