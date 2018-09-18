
from contextlib import contextmanager

import requests
from nanohttp import RegexRouteController, json, settings
from restfulpy.mockup import mockup_http_server
from bddrest import given, status, response

from jaguar.tests.helpers import MockupApplication, AutoDocumentationBDDTest


@contextmanager
def sample_mockup_server():


    class Root(RegexRouteController):
        def __init__(self):
            super().__init__([('/apiv1/obtains', self.obtain,)])

        @json
        def obtain(self):
            return dict(version='1.0.0')

    app = MockupApplication('sample', Root())
    with mockup_http_server(app) as (server, url):
        settings.merge(f'''
            tokenizer:
              url: {url}
        ''')
        yield app


class TestCasClient(AutoDocumentationBDDTest):

    def test_mockup_server(self):
        with sample_mockup_server():
            res = requests.request(
                'OBTAIN',
                f'{settings.tokenizer.url}/apiv1/obtains'
            )
            assert res.status_code == 200
            import pudb; pudb.set_trace()  # XXX BREAKPOINT
            with self.given(
                'Testing mockup server',
                f'{settings.tokenizer.url}/apiv1/obtains',
                'OBTAIN',
            ):
                assert status == 200
                assert response.json['version'] == '1.0.0'


