import asyncio
from os import path

import aio_pika
import aiohttp
import aioredis
import itsdangerous
from aiohttp import web
from nanohttp import settings
from restfulpy.configuration import configure as restfulpy_configure
from restfulpy.principal import JwtPrincipal

from jaguar import Jaguar


class SessionManager:
    _redis = None

    @classmethod
    async def redis(cls):
       if cls._redis is None:
           cls._redis = await aioredis.create_redis(
               f'redis://{settings.authentication.redis.host}:' \
               f'{settings.authentication.redis.port}',
               db=settings.authentication.redis.db,
            )
       return cls._redis

    async def register_session(self, member_id, session_id, queue):
        self._redis.hset(
            f'member:{member_id}',
            session_id,
            queue
        )

    async def get_sessions(self, member_id):
        session_queue = await self._redis.hgetall(f'member:{member_id}')
        active_sessions = [
            (session, queue) for session, queue in session_queue.items()
        ]

        return active_sessions if active_sessions else None

    async def cleanup_session(self, member_id, session_id):
        self._redis.hdel(f'member:{member_id}', session_id)

    async def cleanup_member(self, member_id):
        self._redis.delete(member_id)


session_manager = SessionManager()


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

    await session_manager.redis()
    # Register session
    await session_manager.register_session(
        identity.id,
        identity.session_id,
        app['queue']
    )

    await ws.prepare(request)

    async for msg in ws:
        # TODO: These lines below are completely useless and must be removed before
        # the first version
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
    while True:
        # TODO: pull one by one from the app[queue]
        await asyncio.sleep(1)
        print('Worker tick')


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

    app['queue'] = settings.worker.queue.url
    queue_connection = await aio_pika.connect_robust(app['queue'])
    queue_channel = await queue_connection.channel()


app = web.Application()
app.on_startup.append(configure)
app.add_routes([web.get('/', websocket_handler)])


if __name__ == '__main__':
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    web.run_app(app)

