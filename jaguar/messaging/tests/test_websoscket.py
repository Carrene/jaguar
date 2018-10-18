import pytest
import aiohttp
from multidict import CIMultiDict

from bddrest.authoring import when, Update, Remove, status

from jaguar.models.membership import User
from jaguar.tests.helpers import AutoDocumentationBDDTest, cas_mockup_server


class TestWebsocketConnection(AutoDocumentationBDDTest):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        user = User(
            email='user@example.com',
            title='user',
            access_token='access token',
            reference_id=1
        )
        contact1 = User(
            email='contact1@example.com',
            title='contact1',
            access_token='access token',
            reference_id=2
        )
        user.contacts.append(contact1)
        session.add(user)
        session.commit()

    async def test_websocket(self, websocket_session):
        self.login('user@example.com')

        with pytest.raises(aiohttp.WSServerHandshakeError):
            async with websocket_session() as ws:
               pass

        headers = CIMultiDict()
        headers['Authorization'] = self._authentication_token
        async with websocket_session(headers=headers) as ws:
            await ws.send_str('close')
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print('Server: ', msg.data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break

"""
async def test_websocket(websocket_session):
    with pytest.raises(aiohttp.WSServerHandshakeError):
        await websocket_session()

    headers = CIMultiDict()
    token = ''
    headers['Authorization'] = token
    async with await websocket_session(headers=headers) as ws:
        await ws.send_str('close')
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print('Server: ', msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
"""
