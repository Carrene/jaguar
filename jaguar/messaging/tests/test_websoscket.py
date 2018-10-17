
import aiohttp


async def test_websocket(websocket_session):
    async with websocket_session() as ws:
        await ws.send_str('close')
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                print('Server: ', msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

