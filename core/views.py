import base64
from urllib import parse
from urllib.parse import quote_plus, unquote_plus

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore

from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, redirect


# Create your views here.
from core.models import OAuthLogout
from core.settings import *
from core.settings import get
from core.utils import get_basic_auth_header



def get_url(redirect_url):
    return '{0}?client_id={1}&state=random_state_string&response_type=code&redirect_uri={url_login}'.format(OAUTH_PROVIDER_URL, CLIENT_ID, url_login=redirect_url)

def get_redirect_url(request, double_encoding=True):
    if 'next' not in request.GET:
        raise Http404
    next=quote_plus(request.GET['next'])
    if double_encoding:
        next=quote_plus(next)#TODO: verificar pq é necessário codificar duas vezes para não gerar o erro Error trying to decode a non urlencoded string. Found invalid characters: {'/'} in the string:
    path_login=request.build_absolute_uri(reverse(oauth_login))

    return '{url_login}?next={next}'.format(url_login=path_login, next=next)



def oauth_login(request):
    if 'code' in request.GET:

        authorization_code=request.GET['code']

        user=authenticate(authorization_code=authorization_code, url_redirect=get_redirect_url(request, False))

        login(request, user)
        print('SID_after:'+str(request.session.session_key))

        path_logout=request.build_absolute_uri(reverse(logout_view,  kwargs={'session_key': request.session.session_key}))
        data={'access_token': user.access_token, 'logout_url':path_logout}
        response=requests.get(OAUTH_REGISTER_SESSION, params=data)



        return redirect(unquote_plus(request.GET['next']))
    else:
        return redirect(get_url(get_redirect_url(request)))


@login_required
def teste(request):

    return HttpResponse('Teste Sucesso! usuário logado: {0}<br><a href="http://localhost:8000/logout">logout</a>'.format(request.user))

def logout_view(request, session_key):
    if session_key:
        s=SessionStore(session_key=session_key)
        s.delete()
    else:

        logout(request)
    return HttpResponse(status=200, content='Logout com Sucesso!')
    # if('access_token' in request.POST):
    #     OAuthLogout.objects.create(access_token=request.POST['access_token'])
    #     return HttpResponse(status=200, content='Logout com Sucesso!')
    # else:
    #     return HttpResponse(status=400, content='Necessário informar o access_token!')