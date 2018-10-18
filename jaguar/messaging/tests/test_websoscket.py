import pytest
import aiohttp
from multidict import CIMultiDict


async def test_websocket(websocket_session):
    with pytest.raises(aiohttp.WSServerHandshakeError):
        await websocket_session()
#
#    headers = CIMultiDict()
    import pudb; pudb.set_trace()  # XXX BREAKPOINT
    async with await websocket_session() as ws:
        await ws.send_str('close')
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print('Server: ', msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

