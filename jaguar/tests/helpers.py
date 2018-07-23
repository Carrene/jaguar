from os import path, makedirs

from bddrest.authoring import response
from restfulpy.testing import ApplicableTestCase


HERE = path.abspath(path.dirname(__file__))


<<<<<<< 6f9f35507b04eb354c398daddcb818b5abd00ca5
class AutoDocumentationBDDTest(ApplicableTestCase):
=======
class BDDTestClass(ApplicableTestCase):
>>>>>>> Creating autodocument for jaguar

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
<<<<<<< 6f9f35507b04eb354c398daddcb818b5abd00ca5
            autodump=dump and self.get_spec_filename,
            autodoc=dump and self.get_markdown_filename,
=======
            autodump=self.get_spec_filename if dump else False,
            autodoc=self.get_markdown_filename if dump else False,
>>>>>>> Creating autodocument for jaguar
            *args,
            **kwargs
        )

