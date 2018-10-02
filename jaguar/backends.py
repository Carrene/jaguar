import json

import requests
from nanohttp import settings, HTTPFound, HTTPForbidden

from .exceptions import CASServerNotAvailable, CASServerNotFound, \
    CASInternallError


class CASClient:

    def get_access_token(self, authorization_code):
        if authorization_code is None:
            raise HTTPForbidden()

        response = requests.request(
            settings.oauth.access_token.verb.upper(),
            settings.oauth.access_token.url,
            data=dict(
                code=authorization_code,
                secret=settings.oauth['secret'],
                applicationId=settings.oauth['application_id']
            )
        )
        if response.status_code == 403:
            raise HTTPForbidden()

        if response.status_code == 404:
            raise CASServerNotFound()

        # 502: Bad Gateway
        # 503: Service Unavailbale
        if response.status_code in (502, 503):
            raise CASServerNotAvailable()

        if response.status_code == 500:
            raise CASInternallError()

        result = json.loads(response.text)
        return result['accessToken'], result['memberId']

    def get_member(self, access_token):
        response = requests.request(
            settings.oauth.member.verb.upper(),
            f'{settings.oauth.member.url}/me',
            headers={'authorization': f'oauth2-accesstoken {access_token}'}
        )
        if response.status_code == 403:
            raise HTTPForbidden()

        if response.status_code == 404:
            raise CASServerNotFound()

        # 502: Bad Gateway
        # 503: Service Unavailbale
        if response.status_code in (502, 503):
            raise CASServerNotAvailable()

        if response.status_code == 500:
            raise CASInternallError()

        member = json.loads(response.text)
        return member

