from os import path, makedirs

from restfulpy.application import Application
from bddrest.authoring import response
from restfulpy.testing import ApplicableTestCase
from restfulpy.orm import DBSession

from jaguar import Jaguar
from jaguar.authentication import Authenticator
from jaguar.controllers.root import Root
from jaguar.models.membership import User


HERE = path.abspath(path.dirname(__file__))


class AutoDocumentationBDDTest(ApplicableTestCase):

    __application_factory__ = Jaguar

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

    def login(self, email, url='/apiv1/tokens', verb='CREATE'):
        super().login(dict(email=email), url = url, verb = verb)

