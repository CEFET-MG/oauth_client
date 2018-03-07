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
from oauth_client.settings import *





def get_url(redirect_url):
    return '{0}?client_id={1}&state=random_state_string&response_type=code&redirect_uri={url_login}'.format(OAUTH_PROVIDER_URL, CLIENT_ID, url_login=redirect_url)

def get_redirect_url(request, double_encoding=True):
    if 'next' not in request.GET or not request.GET['next']:
        next=quote_plus('/')
    else:
        next=quote_plus(request.GET['next'])
    if double_encoding:
        next=quote_plus(next)#TODO: verificar pq é necessário codificar duas vezes para não gerar o erro Error trying to decode a non urlencoded string. Found invalid characters: {'/'} in the string:
    path_login=request.build_absolute_uri(reverse(oauth_login))

    return '{url_login}?next={next}'.format(url_login=path_login, next=next)



def oauth_login(request):
    if 'code' in request.GET:

        authorization_code=request.GET['code']
        errors=[]
        user=authenticate(authorization_code=authorization_code, url_redirect=get_redirect_url(request, False), errors=errors)
        if user:
            login(request, user)
            request.session.set_expiry(0) #Define que a sessão do usuário só irá expirar quando o browser fechar.
            print('SID_after:'+str(request.session.session_key))

            path_logout=request.build_absolute_uri(reverse(logout_view,  kwargs={'session_key': request.session.session_key}))
            data={'access_token': user.access_token, 'logout_url':path_logout}
            response=requests.post(OAUTH_REGISTER_SESSION, data=data)
            if(response.status_code==200):
                request.session['session_oauth']=response.json()['session_key']
            else:
                print( 'Falha ao registrar aplicação')
            return redirect(unquote_plus(request.GET['next']))
        else:
            return render(request, ERROR_PAGE, {"error_messages": errors})
    else:
        return redirect(get_url(get_redirect_url(request)))

def logout_view(request, session_key):
    if session_key:
        s=SessionStore(session_key=session_key)
        s.delete()
    else:
        if("session_oauth" in request.session):
            session_oauth=request.session['session_oauth']
            logout(request)
            requests.get('{0}logout/{1}'.format(OAUTH_URL, session_oauth)) #deslogando de todas as outras Aplicações
        else:
            logout(request)


    return redirect(LOGOUT_PAGE) if LOGOUT_PAGE else redirect(get_url(get_redirect_url(request)))
    # if('access_token' in request.POST):
    #     OAuthLogout.objects.create(access_token=request.POST['access_token'])
    #     return HttpResponse(status=200, content='Logout com Sucesso!')
    # else:
    #     return HttpResponse(status=400, content='Necessário informar o access_token!')