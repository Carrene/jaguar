import json
from os import path
from urllib.parse import parse_qsl
import asyncio

import aio_pika
import aiohttp
import itsdangerous
from aiohttp import web
from nanohttp import settings
from restfulpy.configuration import configure as restfulpy_configure
from restfulpy.principal import JwtPrincipal

from jaguar import Jaguar
from queues import queue_manager
from sessions import session_manager
from routing import message_router


async def dequeue_callback(self, message: aio_pika.IncomingMessage):
    with message.process():
        print(message.body)
        await ws.send_str(message.body.decode())


async def authenticate(request):
    query_string_dict = dict(parse_qsl(request.query_string))

    if 'authorization' not in query_string_dict:
        raise web.HTTPUnauthorized()

    encoded_token = query_string_dict['authorization']
    if encoded_token is None or not encoded_token.strip():
        raise web.HTTPUnauthorized()

    try:
        principal = JwtPrincipal.load(encoded_token)
        return principal
    except itsdangerous.BadData:
        raise web.HTTPUnauthorized()


#https://aiohttp.readthedocs.io/en/stable/web_advanced.html#graceful-shutdown
async def websocket_handler(request):

    identity = await authenticate(request)

    ws = web.WebSocketResponse()

    # Register session
    await session_manager.register_session(
        identity.id,
        identity.session_id,
        f'queue:{identity.session_id}'
    )

    # Create the queue related to established session
    await queue_manager.create_queue_async(f'queue:{identity.session_id}')

    app[str(identity.session_id)] = ws

    print(f'Member connected with session id: {identity.session_id}')
    await ws.prepare(request)

    await ws.send_str('hi')

    async for message in queue_manager.queues[f'queue:{identity.session_id}']:
        with message.process():
            print(message.body)
            await ws.send_str(message.body.decode())

    async for msg in ws:

        # TODO: These lines below are completely useless and must be removed
        # before the first version
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.send_str('closing')
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    await session_manager.cleanup_session(identity.id, identity.session_id)

    print('websocket connection closed')
    return ws


async def worker():
    print('Worker stared')
    async with queue_manager._connection_async:
        print('New message')
        async for message in queue_manager.queues['envelops_queue']:
            with message.process():
                print(message.body)
                envelop = json.loads(message.body)
                await message_router.route(envelop)
                print(f'Message dequeued: {envelop}')


async def create_envelop_worker_queue(app):
    await queue_manager.rabbitmq_async
    app['envelops_queue'] = await queue_manager.create_queue_async('envelops_queue')


async def establish_cache_manager_connection(app):
    app['cache_manager'] = await session_manager.redis()


async def start_background_tasks(app):
    app['message_dispatcher'] = app.loop.create_task(worker())


async def cleanup_background_tasks(app):
    app['message_dispatcher'].cancel()
    await app['message_dispatcher']


HERE = path.abspath(path.dirname(__file__))
ROOT = path.abspath(path.join(HERE, '../..'))


async def configure(app):
    _context = {
        'process_name': 'Jaguar Websocket Server',
        'root_path': ROOT,
        'data_dir': path.join(ROOT, 'data'),
    }

    restfulpy_configure(context=_context, force=True)
    settings.merge(Jaguar.__configuration__)
    # FIXME: Configuration file?


app = web.Application()

app.add_routes([web.get('/', websocket_handler)])

app.on_startup.append(configure)
app.on_startup.append(establish_cache_manager_connection)
app.on_startup.append(create_envelop_worker_queue)
app.on_startup.append(start_background_tasks)

app.on_cleanup.append(cleanup_background_tasks)


if __name__ == '__main__':
    web.run_app(app)

