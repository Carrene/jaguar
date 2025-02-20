from aiohttp import web
from easycli import SubCommand, Argument

from ..messaging.websocket import app


DEFAULT_ADDRESS = '8085'


class WebsocketStartSubSubCommand(SubCommand): # pragma: no cover
    __help__ = 'Starts the websocket server.'
    __command__ = 'start'
    __arguments__ = [
        Argument(
            '-b',
            '--bind',
            default=DEFAULT_ADDRESS,
            metavar='{HOST:}PORT',
            help='Bind Address. default: %s' % DEFAULT_ADDRESS,
        ),
    ]

    def __call__(self, args):
        host, port = args.bind.split(':')\
            if ':' in args.bind else ('', args.bind)
        kw = {}
        if port:
            kw['port'] = port

        if host:
            kw['host'] = host

        web.run_app(app, **kw)


class WebsocketSubCommand(SubCommand):  # pragma: no cover
    __help__ = 'Websocket related.'
    __command__ = 'websocket'
    __arguments__ = [
        WebsocketStartSubSubCommand,
    ]

