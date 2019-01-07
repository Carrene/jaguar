import json
from os import path

import aiohttp
import aio_pika
import itsdangerous
from aiohttp import web
from cas import CASPrincipal
from nanohttp import settings
from restfulpy.orm import DBSession
from restfulpy.configuration import configure as restfulpy_configure

from .queues import queue_manager
from .routing import message_router
from .sessions import session_manager


async def authenticate(request):
    encoded_token = request.query.get('token');
    if encoded_token is None:
        raise web.HTTPUnauthorized()

    if encoded_token is None or not encoded_token.strip():
        raise web.HTTPUnauthorized()

    try:
        principal = CASPrincipal.load(encoded_token)
        return principal
    except itsdangerous.BadData:
        raise web.HTTPUnauthorized()


#https://aiohttp.readthedocs.io/en/stable/web_advanced.html#graceful-shutdown
async def websocket_handler(request):
    identity = await authenticate(request)

    member = DBSession.query(Member) \
        .filter(Member.reference_id == identity.reference_id) \
        .one_or_none()
    if member is None:
        raise web.HTTPUnauthorized()

    print('New session: %s has been connected' % identity.session_id)

    await session_manager.register_session(
        member.id,
        identity.session_id,
        settings.rabbitmq.websocket_queue
    )

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    app[str(identity.session_id)] = ws

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.send_str('closing')
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')
    await session_manager.cleanup_session(identity.id, identity.session_id)

    return ws


async def worker(name):
    await queue_manager.queues[name].consume(callback)


async def callback(message: aio_pika.IncomingMessage):
    with message.process():
        decoded_message = json.loads(message.body.decode())
        await app[decoded_message['sessionId']].send_json(decoded_message)


async def route_message(name):
    # FIXME: Remove redis server connection establishing in `route_message`
    # Esbtalish connection with redis server
    await session_manager.redis()

    # Prepare rabbitmq synchronous connection object to get used in
    # `send message`
    queue_manager.create_queue(name)

    await queue_manager.create_queue_async(name)
    await queue_manager.dequeue_async(name, callback_routing)


async def callback_routing(message: aio_pika.IncomingMessage):
    with message.process():
        envelop = json.loads(message.body)
        await message_router.route(envelop)


HERE = path.abspath(path.dirname(__file__))
ROOT = path.abspath(path.join(HERE, '../..'))
async def configure(app, force=True):
    from jaguar import Jaguar
    _context = {
        'process_name': 'Jaguar Websocket Server',
        'root_path': ROOT,
        'data_dir': path.join(ROOT, 'data'),
    }

    restfulpy_configure(context=_context, force=force)
    settings.merge(Jaguar.__configuration__)
    # FIXME: Configuration file?


async def start_background_tasks(app):
    await queue_manager.create_queue_async(settings.rabbitmq.websocket_queue)
    app['message_dispatcher'] = app.loop.create_task(
        worker(settings.rabbitmq.websocket_queue)
    )


async def cleanup_background_tasks(app):
    app['message_dispatcher'].cancel()
    await app['message_dispatcher']


async def establish_cache_manager_connection(app):
    await session_manager.redis()


app = web.Application()
app.add_routes([web.get('/', websocket_handler)])

app.on_startup.append(configure)
app.on_startup.append(establish_cache_manager_connection)
app.on_startup.append(start_background_tasks)

app.on_cleanup.append(cleanup_background_tasks)

