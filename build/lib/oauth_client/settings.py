from django.conf import settings
from django.core.exceptions import ImproperlyConfigured



def get(key, default):
  return getattr(settings, key, default)


if not hasattr(settings, 'OAUTH_URL'):
  raise ImproperlyConfigured('Must define OAUTH_URL')

if not hasattr(settings, 'CLIENT_ID'):
  raise ImproperlyConfigured('Must define CLIENT_ID')

if not hasattr(settings, 'CLIENT_SECRET'):
  raise ImproperlyConfigured('Must define CLIENT_SECRET')

OAUTH_URL=get('OAUTH_URL', None)


OAUTH_PROVIDER_URL = get('OAUTH_PROVIDER_URL','{0}o/authorize'.format(OAUTH_URL))

OAUTH_TOKEN_EXCHANGE = get('OAUTH_TOKEN_EXCHANGE', '{0}o/token/'.format(OAUTH_URL))

CLIENT_ID=get('CLIENT_ID', None)

CLIENT_SECRET = get('CLIENT_SECRET', None)

ERROR_PAGE = get('ERROR_PAGE', 'error_page.html')

OAUTH_GET_USER = get('OAUTH_GET_USER', '{0}api/me'.format(OAUTH_URL))

OAUTH_LOOKUP_USER_FIELD = get('OAUTH_LOOKUP_USER_FIELD', 'username')

OAUTH_REGISTER_SESSION = get('OAUTH_REGISTER_SESSION', '{0}api/register'.format(OAUTH_URL))

OAUTH_USER_ATTR_MAP = get('OAUTH_USER_ATTR_MAP', {
    "username": "username",
    "first_name": "first_name",
    "last_name": "last_name"
})

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '/home/desenv/developer-python/git/third_part_project/oauth_client/templates',
        ],
    },

]

STATIC_URL = '/static/'


'django.contrib.staticfiles'