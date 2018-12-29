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
        return parser

    def launch(self):
        # TODO: The name of the websocket worker queue must be derived from
        # settings
        # FIXME: put `await` before calling the route_message()
        route_message('envelops_queue')


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

