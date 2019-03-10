from nanohttp import settings
from restfulpy.logging_ import get_logger
from requests import request
from requests.exceptions import RequestException


logger = get_logger('webhook')


class Webhook:

    def sent_message(self, room_id):
        try:
            response = request(
                settings.webhooks.sent.verb,
                settings.webhooks.sent.url,
                params=dict(roomId=room_id),
                timeout=settings.webhooks.mentioned.timeout,
            )
            if response.status_code != 204:
                self._bad_thirdparty_response(response.status_code)

        except Exception as ex:
            self._handle_exception(ex)

    def mentioned_member(self, room_id, member_id):
        try:
            response = request(
                settings.webhooks.mentioned.verb,
                settings.webhooks.mentioned.url,
                params=dict(roomId=room_id, memberId=member_id),
                timeout=settings.webhooks.mentioned.timeout,
            )
            if response.status_code != 204:
                self._bad_thirdparty_response(response.status_code)

        except Exception as ex:
            self._handle_exception(ex)

    def _handle_exception(self, ex):
        if isinstance(ex, RequestException):
            logger.exception('Request Error')

    def _bad_thirdparty_response(self, code):
        logger.exception(
            f'Third party exception with {code} status'
        )

