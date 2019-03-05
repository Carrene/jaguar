from nanohttp import settings
from restfulpy.logging_ import get_logger
from requests import request
from requests.exceptions import ConnectionError, HTTPError, Timeout


logger = get_logger('webhook')


class Webhook:

    def sent_message(self, room_id):
        try:
            response = request(
                settings.webhooks.sent.verb,
                settings.webhooks.sent.url,
                params=dict(roomId=room_id),
                timeout=settings.request.timeout,
            )
            if response.status_code != 200:
                self._bad_thirdparty_response(response.code)

        except Exception as ex:
            self._handle_exception(ex)

    def mentioned_member(self, room_id, member_id):
        try:
            response = request(
                settings.webhooks.mentioned.verb,
                settings.webhooks.mentioned.url,
                params=dict(roomId=room_id, memberId=member_id),
                timeout=settings.request.timeout,
            )
            if response.status_code != 200:
                self._bad_thirdparty_response(response.code)

        except Exception as ex:
            self._handle_exception(ex)

    def _handle_exception(self, ex):
        if isinstance(ex, ConnectionError):
            logger.exception('Connection Error')

        elif isinstance(ex, HTTPError):
            logger.exception('HTTP Error')

        elif isinstance(ex, Timeout):
            logger.exception('Timeout Error')

    def _bad_thirdparty_response(code):
        logger.exception(
            f'Third party exception with {code} status'
        )

