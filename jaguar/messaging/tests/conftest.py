import asyncio
from async_generator import asynccontextmanager

import pytest
import aiohttp
from multidict import CIMultiDict
from aiohttp.web_runner import AppRunner, TCPSite
from nanohttp.tests.conftest import free_port

from jaguar.tests.helpers import AutoDocumentationBDDTest
from jaguar.messaging.websocket import app as websocket_application
from jaguar.messaging import queues, sessions, router
from jaguar import asyncdb


@pytest.fixture
async def websocket_server(loop, free_port):
    host = 'localhost'
    runner = AppRunner(websocket_application)
    await runner.setup()
    tcpsite = TCPSite(runner, host, free_port, shutdown_timeout=2)
    await tcpsite.start()

    yield tcpsite.name

    await runner.shutdown()
    await runner.cleanup()


@pytest.fixture
async def websocket_session(websocket_server):
    @asynccontextmanager
    async def connect(token=None, **kw):
        query_string = ''
        if token:
            query_string = f'token={token}'

        async with aiohttp.ClientSession() as session, \
                session.ws_connect(websocket_server + f'?{query_string}') as ws:
            yield ws
    yield connect


class AsyncTest(AutoDocumentationBDDTest):
    def setup(self):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            return

        async def do_():
            await sessions.dispose()
            await sessions.flush_all()
            await queues.dispose_async()
            await queues.flush_all_async()
            await asyncdb.close_connection()

        loop.run_until_complete(do_())


    def teardown(self):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            return

        async def do_():
            await sessions.dispose()
            await sessions.flush_all()
            await queues.dispose_async()
            await queues.flush_all_async()
            await asyncdb.close_connection()

        loop.run_until_complete(do_())


