import asyncio

from aiohttp import web
from restfulpy.cli import Launcher, RequireSubCommand

from .websocket import app, route_message


DEFAULT_ADDRESS = '8085'


class RouterStartLauncher(Launcher): # pragma: no cover
    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'start',
            help='Starts the message router.'
        )
        parser.add_argument(
            '-q',
            '--queue',
            default='workers',
            help='The queue name of fetching envelops from database'
        )
        return parser

    def launch(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(route_message(self.args.queue))
        except:
            # The value returned is based on UNIX-like cli applications
            return 1


class MessageRouterLauncher(Launcher, RequireSubCommand):
    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('router', help='Message router.')
        router_subparsers = parser.add_subparsers(
            title='Message router',
            dest='router_command'
        )
        RouterStartLauncher.register(router_subparsers)
        return parser


class WebsocketStartLauncher(Launcher): # pragma: no cover
    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'start',
            help='Starts the websocket server.'
        )
        parser.add_argument(
            '-b',
            '--bind',
            default=DEFAULT_ADDRESS,
            metavar='{HOST:}PORT',
            help='Bind Address. default: %s' % DEFAULT_ADDRESS
        )
        return parser

    def launch(self):
        host, port = self.args.bind.split(':')\
            if ':' in self.args.bind else ('', self.args.bind)
        kw = {}
        if port:
            kw['port'] = port

        if host:
            kw['host'] = host

        web.run_app(app, **kw)


class WebsocketLauncher(Launcher, RequireSubCommand):  # pragma: no cover
    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('websocket', help='Websocket related.')
        websocket_subparsers = parser.add_subparsers(
            title='Websocket server administration.',
            dest='websocket_command'
        )
        WebsocketStartLauncher.register(websocket_subparsers)
        return parser

