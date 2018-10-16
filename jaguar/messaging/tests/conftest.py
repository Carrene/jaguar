import aiohttp
from nanohttp.tests.conftest import free_port


pytest_plugins = ['aiohttp.pytest_plugin']
from ..websocket import app

def websocket_server(free_port):
    loop = asyncio.get_event_loop()
    if asyncio.iscorutine(app):


