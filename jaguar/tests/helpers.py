from os import path, makedirs

from bddrest.authoring import response
from restfulpy.testing import ApplicableTestCase


HERE = path.abspath(path.dirname(__file__))


class AutoDocumentationBDDTest(ApplicableTestCase):

    @classmethod
    def get_spec_filename(cls, story):
        filename = f'{story.base_call.verb}-' \
                   f'{story.base_call.url.split("/")[2]}({story.title})'
        target = path.abspath(path.join(HERE, '../../data/specifications'))
        if not path.exists(target):
            makedirs(target, exist_ok=True)
        filename = path.join(target, f'{filename}.yml')
        return filename

    @classmethod
    def get_markdown_filename(cls, story):
        filename = f'{story.base_call.verb}-' \
                   f'{story.base_call.url.split("/")[2]}({story.title})'
        target = path.abspath(path.join(HERE, '../../data/documentation'))
        if not path.exists(target):
            makedirs(target, exist_ok=True)
        filename = path.join(target, f'{filename}.md')
        return filename

    def given(self, title, dump=True, *args, **kwargs):
        return super().given(
            title = title,
            autodump=dump and self.get_spec_filename,
            autodoc=dump and self.get_markdown_filename,
            *args,
            **kwargs
        )

