
import pytest
from nanohttp import settings
from jaguar.webhooks import Webhook
from requests import RequestException

from jaguar.tests.helpers import thirdparty_mockup_server, \
    AutoDocumentationBDDTest


class TestSentWebhook(AutoDocumentationBDDTest):

    def test_webhook_sent_message(self, request):
        webhook = Webhook()

        # No raise
        with thirdparty_mockup_server():
            webhook.sent_message(1)

            # When thirdparty response with status != 204
            webhook.sent_message('bad')

            # When a request error occur
            settings.merge(f'''
              webhooks:
                sent:
                  url: invalid-url
            ''')
            webhook.sent_message(1)

