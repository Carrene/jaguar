import aioredis
from nanohttp import settings
from restfulpy.principal import JwtPrincipal

from jaguar.messaging.websocket import SessionManager
from jaguar.models import Member
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

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        member = Member(
            email='member@example.com',
            title='member',
            access_token='access token',
            reference_id=1
        )
        session.add(member)
        session.commit()

    def setup(self):
        redis.flushdb()

    async def test_register(self, websocket_session):
        self.setup()
        self.login('member@example.com')

        token = JwtPrincipal.load(self._authentication_token)
        session_manager = SessionManager(redis)

        async with websocket_session(token=self._authentication_token) as ws:

            # Get sessions by member id
            active_sessions = await session_manager.get_sessions(token.id)
            assert active_sessions[0] == (token.id, token.session_id)

            # Clean up session
            await session_manager.cleanup_session(session=token.session_id)

            # Get sessions by member id
            active_sessions = await session_manager.get_sessions(
                member=token.id
            )
            assert active_sessions[0] == None

            # Teardown Redis DB
            await redis.flushdb()

            assert 1 == 1


