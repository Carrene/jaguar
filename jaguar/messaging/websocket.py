import asyncio
from os import path

import aiohttp
import itsdangerous
from aiohttp import web
from restfulpy.principal import JwtPrincipal
from restfulpy.configuration import configure as restfulpy_configure
from nanohttp import settings


from jaguar import Jaguar


class SessionManager:

    def __init__(self, cache_manager):
        self.cache_manager = cache_manager

    @staticmethod
    def register_session(app, member_id, session_id, socket):
        if member_id not in app['members']:
            app['members'][member_id] = []

        member_sessions = app['members'][member_id]
        if session_id not in member_sessions:
            member_sessions.append(session_id)
        app['sessions'][session_id] = (member_id, socket)

    @staticmethod
    def unregister_session(app, session_id):
        sessions = app['sessions']
        if session_id in sessions:
            member, socket = app['sessions'][session_id]
            del app['sessions'][session_id]
            app['members'][member_id].remove(session_id)


async def authenticate(request):
    if 'Authorization' not in request.headers:
        raise web.HTTPUnauthorized()

    encoded_token = request.headers['Authorization']
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
    await ws.prepare(request)

    member_id = context.identity.id
    session_id = context.identity.session_id

    SessionManager.register_session(request.app, member_id, session_id, ws)
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
    SessionManager.unregister_session(request.app, session_id)

    return ws


async def worker():
    while True:
        await asyncio.sleep(1)
        print('Worker tick')


async def start_background_tasks(app):
    app['message_dispatcher'] = app.loop.create_task(worker())


async def cleanup_background_tasks(app):
    app['message_dispatcher'].cancel()
    await app['message_dispatcher']


HERE = path.abspath(path.dirname(__file__))
ROOT = path.abspath(path.join(HERE, '../..'))


async def configure(app, force=None):
    _context = {
        'process_name': 'Jaguar Websocket Server',
        'root_path': ROOT,
        'data_dir': path.join(ROOT, 'data'),
    }

    restfulpy_configure(context=_context, force=force)
    settings.merge(Jaguar.__configuration__)
    # FIXME: Configuration file?


app = web.Application()
#app.on_startup.append(configure)
app.add_routes([web.get('/', websocket_handler)])


if __name__ == '__main__':
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    web.run_app(app)

