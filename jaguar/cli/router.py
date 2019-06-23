import asyncio

from easycli import SubCommand, Argument
from nanohttp import settings

from ..messaging.router import start as start_router


class RouterStartLauncher(SubCommand): # pragma: no cover
    __help__ = 'Starts the message router.'
    __command__ = 'start'

    def __call__(self, args):
        loop = asyncio.get_event_loop()
        queue = settings.messaging.workers_queue
        print(f'Listenning on: {queue}')
        loop.run_until_complete(start_router(queue))


class RouterLauncher(SubCommand):
    __help__ = 'Message router.'
    __command__ = 'router'
    __arguments__ = [
        RouterStartLauncher,
    ]

