import pytest

from nanohttp import settings, contexts
from restfulpy.configuration import configure
from restfulpy import Application
from restfulpy.orm import DBSession
from restfulpy.db import DatabaseManager
from restfulpy.orm import setup_schema, session_factory, create_engine


class DatabaseManger:

    session = None
    engine = None

    def __init__(self, configuration):
        self.configure(configuration)

    def configure(self, configuration):
        configure(configuration, context=dict())
        settings.db.url = settings.db.test_url

    @classmethod
    def connect(cls) -> 'Session':
        cls.engine = create_engine()
        cls.session = session =session_factory(
            bind=cls.engine,
            expire_on_commit=False
        )

    @classmethod
    def close_all_connections(cls):
        cls.session.close_all()
        cls.engine.dispose()

    def drop_database(self):
        with DatabaseManager() as m:
            m.drop_database()

    def create_database(self):
        with DatabaseManager() as m:
            m.create_database()

    @classmethod
    def create_schema(cls):
        setup_schema(cls.session)
        cls.session.commit()



@pytest.fixture
def db():

    print('Setup')

    builtin_configuration = '''
    db:
      test_url: postgresql://postgres:postgres@localhost/panda_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres
    logging:
      loggers:
        default:
          level: critical
    '''

    # configure
    database_manger = DatabaseManger(builtin_configuration, force=True)

    # drop
    database_manger.drop_database()

    # create
    database_manger.create_database()

    # connect
    database_manger.connect()

    # schema
    database_manger.create_schema()

    #tear dwon
    yield database_manger
    print('Tear down')

    # close all connections
    database_manger.close_all_connections()

    # Drop Db
    database_manger.drop_database()

