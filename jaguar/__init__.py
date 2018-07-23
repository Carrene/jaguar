from os.path import join, dirname

from restfulpy.application import Application

from .authentication import Authenticator
from .controllers.root import Root
from jaguar.cli.email import EmailLauncher

__version__ = '0.1.0-dev'


class Jaguar(Application):
    __authenticator__ = Authenticator()

    __configuration__ = """
    
    db:
      url: postgresql://postgres:postgres@localhost/jaguar_dev
      test_url: postgresql://postgres:postgres@localhost/jaguar_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres
    
    messaging:
      default_messenger: restfulpy.messaging.SmtpProvider
    
    smtp:
      host: mail.carrene.com
      port: 587
      username: nc@carrene.com
      password: <smtp-password>
      local_hostname: carrene.com

    activation:
      secret: activation-secret
      max_age: 86400  # seconds
      url: http://nc.carrene.com/activate
      # url: http://localhost:8080/activate
      """

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

