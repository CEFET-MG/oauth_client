from django.conf.urls import url
from oauth_client.views import *

urlpatterns = [
    url(r'^oauth/login$', oauth_login, name='oauth_login'),
    url(r'^logout/(?P<session_key>.*)$', logout_view, name='logout'),

]
