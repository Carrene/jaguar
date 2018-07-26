from os.path import join, dirname

from restfulpy.application import Application

from .authentication import Authenticator
from .controllers.root import Root
from jaguar.cli.email import EmailLauncher


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
      url: http://ecample.com/activate

    '''

    def __init__(self):
        super().__init__(
            'jaguar',
            root=Root(),
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )

    # noinspection PyArgumentList
    def insert_mockup(self, *args):
        mockup.insert()
        DBSession.commit()

    def register_cli_launchers(self, subparsers):
        EmailLauncher.register(subparsers)


jaguar = Jaguar()

