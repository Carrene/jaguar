import json
from os import path

import aiohttp
import itsdangerous
from aiohttp import web
from cas import CASPrincipal
from nanohttp import settings
from restfulpy.orm import DBSession
from restfulpy.configuration import configure as restfulpy_configure

from . import queues
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

    member_id = DBSession.query(Member.id) \
        .filter(Member.reference_id == identity.reference_id) \
        .one_or_none()
    if member_id is None:
        raise web.HTTPUnauthorized()

    print('New session: %s has been connected' % identity.session_id)

    await session_manager.register_session(
        member_id[0],
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
    # Prepare rabbitmq synchronous connection object to get used in
    # `send message`
    while True:
        message = await queue_manager.pop_async(name)
        decoded_message = json.loads(message.body.decode())
        await app[decoded_message['sessionId']].send_json(decoded_message)



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


async def start_workers(app):
    await queue_manager.create_queue_async(settings.rabbitmq.websocket_queue)
    app['message_dispatcher'] = app.loop.create_task(
        worker('jaguar_websocket_server_1')
    )


async def cleanup_background_tasks(app):
    app['message_dispatcher'].cancel()
    await app['message_dispatcher']


async def prepare_session_manager(app):
    await session_manager.redis()


app = web.Application()
app.add_routes([web.get('/', websocket_handler)])

app.on_startup.append(configure)
app.on_startup.append(prepare_session_manager)
app.on_startup.append(start_workers)

app.on_cleanup.append(cleanup_background_tasks)

