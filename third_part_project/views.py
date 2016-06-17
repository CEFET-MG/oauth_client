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
from oauth_client.settings import get
from oauth_client.utils import get_basic_auth_header



@login_required
def teste(request):

    return HttpResponse('Teste Sucesso! usuário logado: {0}<br><a href="http://localhost:8000/logout">logout</a>'.format(request.user))
