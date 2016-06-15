import requests
from django.contrib.auth import logout
from django.shortcuts import redirect

from core.models import OAuthLogout


class OauthMiddleWare(object):
    url='http://localhost:8000/o/authorize?client_id=s3t0YNzG4vOLn2XhSRpIJ8yirejgfsPYECFd3jFF&state=random_state_string&response_type=token'
    def process_request(self, request):
        #se ainda não possui usuário autenticado tenta autenticar no servidor oauth
        if hasattr(request, 'user') and request.user.is_authenticated() and 'access_token' in request.session:
            logout_list=OAuthLogout.objects.filter(access_token=request.session['access_token'])
            if logout_list:
                logout_list[0].delete() #remove o registro da fila de logout e desloga o usuário
                logout(request)

        print(request.session.session_key)
        # if user:
        #     request.user = request._cached_user = user


    def authenticate(self):
        redirect(self.url)
