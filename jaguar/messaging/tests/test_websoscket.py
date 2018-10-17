import asyncio

import pytest
import aiohttp


async def test_websocket(websocket_server):
    print(websocket_server)
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(websocket_server) as ws:
            await ws.send_str('close')
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    print('Server: ', msg.data)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
