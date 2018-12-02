import asyncio

import pytest
import aiohttp
from bddrest.authoring import when, Update, Remove, status

from jaguar.models import Member
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestWebsocketConnection(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        cls.loop = asyncio.get_event_loop()

    async def test_websocket(self, websocket_session):
        redis_ =


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

