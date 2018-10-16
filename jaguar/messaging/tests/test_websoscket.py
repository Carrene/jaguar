import asyncio


async def test_websocket(free_port):
    print(free_port)
#    async with session.ws_connect('http://example.org/ws') as ws:
#        async for msg in ws:
#            if msg.type == aiohttp.WSMsgType.TEXT:
#                if msg.data == 'close cmd':
#                    await ws.close()
#                    break
#                else:
#                    await ws.send_str(msg.data + '/answer')
#            elif msg.type == aiohttp.WSMsgType.ERROR:
#                break

