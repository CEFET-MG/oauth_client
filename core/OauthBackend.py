from urllib.parse import quote_plus

from django.contrib.auth.models import User
import requests

from core.settings import OAUTH_TOKEN_EXCHANGE, CLIENT_ID, CLIENT_SECRET, OAUTH_GET_USER
from core.utils import get_basic_auth_header


def get_or_create_user(username):
    return User.objects.get_or_create(username=username)

class OauthBackend(object):


    def authenticate(self, authorization_code, url_redirect):
        token_request_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': url_redirect
        }

        response=requests.post(OAUTH_TOKEN_EXCHANGE, data=token_request_data, headers=get_basic_auth_header(CLIENT_ID, CLIENT_SECRET))

        if(response.status_code==200):
            access_token=response.json()['access_token']
            user_oauth=requests.get('{0}?access_token={1}'.format(OAUTH_GET_USER, access_token)).json()
            user=get_or_create_user(user_oauth['username'])

            user[0].backend=self
            user[0].access_token=access_token

            return user[0]



    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None