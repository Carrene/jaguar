from aiohttp import web
from restfulpy.cli import Launcher, RequireSubCommand

from .websocket import app


class WebsocketStartLauncher(Launcher):  # pragma: no cover
    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'start',
            help='Starts the websocket server.'
        )
        return parser

    def launch(self):
        web.run_app(app)


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

