
import pytest
from nanohttp import settings
from jaguar.webhooks import Webhook
from requests import RequestException

from jaguar.tests.helpers import thirdparty_mockup_server, \
    AutoDocumentationBDDTest


class TestMentionedWebhook(AutoDocumentationBDDTest):

    def test_webhook_mentioned_message(self, request):
        webhook = Webhook()

        # No raise
        with thirdparty_mockup_server():
            webhook.mentioned_member(1, 1)

            # When thirdparty response with status != 200
            webhook.mentioned_member('bad', 'bad')

            # When a request error occur
            settings.merge(f'''
              webhooks:
                mentioned:
                  url: invalid-url
            ''')
            webhook.mentioned_member(1, 1)

