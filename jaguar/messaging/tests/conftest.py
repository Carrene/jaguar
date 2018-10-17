import pytest
import aiohttp
from aiohttp.web_runner import AppRunner, TCPSite
from nanohttp.tests.conftest import free_port


pytest_plugins = ['aiohttp.pytest_plugin']
from ..websocket import app as websocket_application


@pytest.fixture
async def websocket_server(loop, free_port):
    #loop = asyncio.get_event_loop()
    host = 'localhost'
    runner = AppRunner(websocket_application)
    await runner.setup()
    tcpsite = TCPSite(runner, host, free_port, shutdown_timeout=2)
    await tcpsite.start()

    yield tcpsite.name

    await runner.shutdown()
    await runner.cleanup()

