from os import path, makedirs

from restfulpy.application import Application
from bddrest.authoring import response
from restfulpy.testing import ApplicableTestCase
from restfulpy.orm import DBSession

from jaguar.authentication import Authenticator
from jaguar.controllers.root import Root
from jaguar.models.membership import User

HERE = path.abspath(path.dirname(__file__))


class AutoDocumentationBDDTest(ApplicableTestCase):

    __application__ = Application(
        'Mockup',
        root=Root(),
        authenticator=Authenticator()
    )

    __configuration__ = '''
    db:
      url: postgresql://postgres:postgres@localhost/jaguar_dev
      test_url: postgresql://postgres:postgres@localhost/jaguar_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres


    activation:
      secret: activation-secret
      max_age: 86400  # seconds
      url: http://nc.carrene.com/activate

    '''

    @classmethod
    def mockup(cls):
        user = User(
            email='already.added@example.com',
            title='example',
            password='123456',
        )
        user.is_active = True
        DBSession.add(user)
        DBSession.commit()

    @classmethod
    def get_spec_filename(cls, story):
        filename = \
            f'{story.base_call.verb}-' \
            f'{story.base_call.url.split("/")[2]}({story.title})'
        target = \
            path.abspath(path.join(HERE, '../../data/specifications'))
        if not path.exists(target):
            makedirs(target, exist_ok=True)
        filename = path.join(target, f'{filename}.yml')
        return filename

    @classmethod
    def get_markdown_filename(cls, story):
        filename = \
            f'{story.base_call.verb}-' \
            f'{story.base_call.url.split("/")[2]}({story.title})'
        target = \
            path.abspath(path.join(HERE, '../../data/documentation'))
        if not path.exists(target):
            makedirs(target, exist_ok=True)
        filename = path.join(target, f'{filename}.md')
        return filename

    def given(self, *args, dump=True, **kwargs):
        return super().given(
            *args,
            autodump=dump and self.get_spec_filename,
            autodoc=dump and self.get_markdown_filename,
            **kwargs
        )
