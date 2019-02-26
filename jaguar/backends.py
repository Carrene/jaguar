import json

import requests
from nanohttp import settings, HTTPFound, HTTPForbidden, HTTPUnauthorized, \
    HTTPStatus

from .exceptions import CASServerNotAvailable, CASServerNotFound, \
    CASInternallError


class CASClient:

    def get_access_token(self, authorization_code):
        if authorization_code is None:
            raise HTTPForbidden()

        response = requests.request(
            'CREATE',
            f'{settings.oauth.url}/apiv1/accesstokens',
            data=dict(
                code=authorization_code,
                secret=settings.oauth['secret'],
                applicationId=settings.oauth['application_id']
            )
        )
        if response.status_code == 404:
            raise CASServerNotFound()

        # 502: Bad Gateway
        # 503: Service Unavailbale
        if response.status_code in (502, 503):
            raise CASServerNotAvailable()

        if response.status_code == 500:
            raise CASInternallError()

        if response.status_code != 200:
            raise HTTPUnauthorized()

        result = json.loads(response.text)
        return result['accessToken'], result['memberId']

    def get_member(self, access_token):
        response = requests.request(
            'GET',
            f'{settings.oauth.url}/apiv1/members/me',
            headers={'authorization': f'oauth2-accesstoken {access_token}'}
        )

        if response.status_code == 404:
            raise CASServerNotFound()

        # 502: Bad Gateway
        # 503: Service Unavailbale
        if response.status_code in (502, 503):
            raise CASServerNotAvailable()

        if response.status_code == 500:
            raise CASInternallError()

        if response.status_code != 200:
            raise HTTPUnauthorized()

        member = json.loads(response.text)
        return member


class DolphinClient:

    def unsee_issue(self, room_id):
        response = requests.request(
            'UNSEE',
            f'{settings.dolphin.url}/apiv1/issues',
            params=dict(roomID=room_id)
        )

        if response.status_code == 618:
            raise HTTPStatus(f'802 Issue With target id {room_id} Not Found')
        elif response.status_code == 779:
            raise HTTPStatus('803 Target Id Is None')
        elif response.status_code == 780:
            raise HTTPStatus('804 Target Id Not In Form')
        elif response.status_code == 781:
            raise HTTPStatus('805 Invalid Target Id type')

        issue = json.loads(response.text)
        return issue

