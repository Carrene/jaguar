from os.path import join, dirname
import functools

from nanohttp import settings
from restfulpy.application import Application
from sqlalchemy_media import StoreManager, FileSystemStore

from .authentication import Authenticator
from .controllers.root import Root
from .cli.email import EmailLauncher


__version__ = '0.1.0-dev'


class Jaguar(Application):
    __authenticator__ = Authenticator()
    __configuration__ = '''

    db:
      url: postgresql://postgres:postgres@localhost/jaguar_dev
      test_url: postgresql://postgres:postgres@localhost/jaguar_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres

    messaging:
      default_messenger: restfulpy.messaging.ConsoleMessenger
      template_dirs:
        - %(root_path)s/jaguar/email_templates

    smtp:
      host: smtp.gmail.com
      username: user@example.com
      password: <smtp-password>
      localhost: gmail.com

    activation:
      secret: activation-secret
      max_age: 86400  # seconds
      url: http://example.com/activate

    oauth:
      secret: oauth2-secret
      application_id: 1
      url: http://localhost:8080

    storage:
      file_system_dir: %(root_path)s/data/assets
      base_url: http://localhost:8080/assets

    '''

    def __init__(self, application_name='jaguar', root=Root()):
        super().__init__(
            application_name,
            root=root,
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )

    # noinspection PyArgumentList
    def insert_mockup(self, *args):
        mockup.insert()
        DBSession.commit()

    def register_cli_launchers(self, subparsers):
        EmailLauncher.register(subparsers)

    @classmethod
    def initialize_orm(cls, engine=None):
        StoreManager.register(
            'fs',
            functools.partial(
                FileSystemStore,
                settings.storage.file_system_dir,
                base_url=settings.storage.base_url,
            ),
            default=True
        )
        super().initialize_orm(cls, engine)

jaguar = Jaguar()

