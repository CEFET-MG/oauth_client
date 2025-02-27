from urllib.parse import quote_plus

from django.contrib.auth.models import User
import requests
from django.core.exceptions import ImproperlyConfigured

from oauth_client.settings import OAUTH_TOKEN_EXCHANGE, CLIENT_ID, CLIENT_SECRET, OAUTH_GET_USER, OAUTH_USER_ATTR_MAP, \
    OAUTH_LOOKUP_USER_FIELD
from django.contrib.auth import get_user_model

from oauth_client.utils import get_basic_auth_header

UserModel = get_user_model()

def get_or_create_user(lookup_field, **attr):

    lookup = {lookup_field: attr[lookup_field]}

    return UserModel.objects.update_or_create(defaults=attr, **lookup)

class OauthBackend(object):

    def user_is_valid(self, oauth_response, erros=[]):
        return True

    def post_create(self, user):
        pass

    def authenticate(self, authorization_code, url_redirect, errors=[]):

        token_request_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': url_redirect
        }

        response=requests.post(OAUTH_TOKEN_EXCHANGE, data=token_request_data, headers=get_basic_auth_header(CLIENT_ID, CLIENT_SECRET))

        if(response.status_code==200):
            access_token=response.json()['access_token']
            me=requests.get('{0}?access_token={1}'.format(OAUTH_GET_USER, access_token))
            if me.status_code!=200:
                print("Error api/me status code: {0}".format(me.status_code));
                return None
            user_oauth=me.json()
            if 'error' in user_oauth:# verifica se deu erro na hora de pegar o usuário
                print(user_oauth['error'])
                errors.append(user_oauth['error'])
                return None

            #Verifica se o usuário é válido antes de criar no banco da aplicação. Usado para facilitar a customização das regras de autenticação
            if self.user_is_valid(user_oauth, errors):
                #Faz o mapeamento entre os atributos do servidor de autenticação e o modelo usuário na aplicação
                attr = {k: user_oauth[v] for k, v in OAUTH_USER_ATTR_MAP.items()}
                #verifica qual o atributo deve ser usado para procurar o usuário correspondente
                if OAUTH_LOOKUP_USER_FIELD  not in attr:
                    raise ImproperlyConfigured('Cannot find OAUTH_LOOKUP_USER_FIELD in user map attributes')

                user=get_or_create_user(OAUTH_LOOKUP_USER_FIELD, **attr)

                print(user_oauth)
                user[0].backend=self
                user[0].access_token=access_token
                user[0].oauth_response=user_oauth
                self.post_create(user[0])
                return user[0]



    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None