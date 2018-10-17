import pytest
import aiohttp
from aiohttp.web_runner import AppRunner, TCPSite
from nanohttp.tests.conftest import free_port


pytest_plugins = ['aiohttp.pytest_plugin']
from ..websocket import app as websocket_application


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
    async with aiohttp.ClientSession() as session:
        def connect(**kw):
            return session.ws_connect(websocket_server, **kw)
        yield connect

