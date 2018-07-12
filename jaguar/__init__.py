from os.path import join, dirname

from restfulpy import Application as BaseApplication


from .controllers.root import Root

__version__ = '0.1.0-dev'


class Application(BaseApplication):

    builtin_configuration = """
        db:
          url: postgresql://postgres:postgres@localhost/jaguar_dev
          test_url: postgresql://postgres:postgres@localhost/jaguar_test
          administrative_url: postgresql://postgres:postgres@localhost/postgres

        jwt:
          secret: JWT-SECRET
          algorithm: HS256
          max_age: 86400  # 24 Hours
          refresh_token:
            secret: JWT-REFRESH-SECRET
            algorithm: HS256
            max_age: 2678400  # 30 Days
            secure: true
            httponly: false

"""
    def __init__(self):
        super().__init__(
            'jaguar',
            root=Root(),
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )

    # noinspection PyArgumentList
    # def insert_basedata(self):
     #    basedata.insert()

    # noinspection PyArgumentList
    # def insert_mockup(self, *args):
     #    mockup.insert()


jaguar = Application()
