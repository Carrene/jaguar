import asyncio

import pytest
import aiohttp


@pytest.mark.asyncio
async def test_websocket(loop, websocket_server):
    print(websocket_server)
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.ws_connect(websocket_server) as ws:
            await ws.send_str('close')
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print('Server: ', msg.data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break

