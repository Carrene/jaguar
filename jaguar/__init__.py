import functools
from os.path import join, dirname

from restfulpy.application import Application
from sqlalchemy_media import StoreManager, FileSystemStore
from nanohttp import settings

from .authentication import Authenticator
from .controllers.root import Root
from .cli.email import EmailLauncher
from .messaging.cli import WebsocketLauncher, MessageRouterLauncher


__version__ = '0.5.2nightly'


class Jaguar(Application):
    __authenticator__ = Authenticator()
    __configuration__ = '''

    db:
      url: postgresql://postgres:postgres@localhost/jaguar_dev
      test_url: postgresql://postgres:postgres@localhost/jaguar_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres

    activation:
      secret: activation-secret
      max_age: 86400  # seconds
      url: http://example.com/activate

    oauth:
      secret: A1dFVpz4w/qyym+HeXKWYmm6Ocj4X5ZNv1JQ7kgHBEk=
      application_id: 1
      url: http://localhost:8083

    storage:
      local_directory: %(root_path)s/data/assets
      base_url: http://localhost:8080/assets

    messaging:
        workers_queue: jaguar_workers
        redis:
            host: localhost
            port: 6379
            password: ~
            db: 1

    '''

    def __init__(self, application_name='jaguar', root=Root()):
        super().__init__(
            application_name,
            root=root,
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )

    def insert_mockup(self, *args):
        mockup.insert()
        DBSession.commit()

    def register_cli_launchers(self, subparsers):
        EmailLauncher.register(subparsers)
        WebsocketLauncher.register(subparsers)
        MessageRouterLauncher.register(subparsers)

    @classmethod
    def initialize_orm(cls, engine=None):
        StoreManager.register(
            'fs',
            functools.partial(
                FileSystemStore,
                settings.storage.local_directory,
                base_url=settings.storage.base_url,
            ),
            default=True
        )
        super().initialize_orm(cls, engine)


jaguar = Jaguar()

