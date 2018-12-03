import asyncio

import pytest
import aiohttp
from bddrest.authoring import when, Update, Remove, status

from jaguar.models import Member
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestWebsocketConnection(AutoDocumentationBDDTest):

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

