from contextlib import asynccontextmanager

import pytest
import aiohttp
from multidict import CIMultiDict
from aiohttp.web_runner import AppRunner, TCPSite
from nanohttp.tests.conftest import free_port


pytest_plugins = ['aiohttp.pytest_plugin']
from jaguar.messaging.websocket import app as websocket_application
from jaguar.tests.helpers import AutoDocumentationBDDTest


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
        if token:
            headers = CIMultiDict()
            headers['Authorization'] = token
            kw['headers'] = headers

        async with aiohttp.ClientSession() as session, \
                session.ws_connect(websocket_server, **kw) as ws:
            yield ws
    yield connect

