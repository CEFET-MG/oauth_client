Inicie
=========================================



Instalação
########################

Baixando o código do repositório
------------------------
.. sourcecode:: sh

    $ git clone gitlab@gitlab.ep.sgi.cefetmg.br:django/oauth_client.git

Instalando o módulo
-----------------------
De dentro da pasta do projeto execute:

.. sourcecode:: sh

    $ python setup.py install


Configuração
########################

Adicione oauth_client em INSTALLED_APPS
----------------------------------

::

    INSTALLED_APPS = (
        # ...
        'oauth_client',
    )       

Adicione o OauthBackend em AUTHENTICATION_BACKENDS
----------------------------------
.. note:: A ordem faz diferença. Caso queira que sua aplicação realize a autenticação apenas via oauth, deixe apenas o OauthBackend na lista.

::

    AUTHENTICATION_BACKENDS = (
        'oauth_client.OauthBackend.OauthBackend',
        # ...
    ) 

Altere a URL da página de login
--------------------------------

::

    LOGIN_URL = '/oauth/login'

Altere a URL da página de erro padrão
--------------------------------

É possivel criar uma página de erro customizada para sua aplicação. Utilize a variável **error_messages** para acessar as mensagens de erro
::

    ERROR_PAGE = 'error_page2.html'
Configurando as variáveis obrigatórias
--------------------------------

Altere os valores do **CLIENT_ID** e **CLIENT_SECRET** para os da **sua aplicação**
::

    OAUTH_URL='http://localhost:8000/'

    CLIENT_ID='y2ROmF4FwkKTiLq2vgSZvsqeX6pqjkYgEJXm4SMw'

    CLIENT_SECRET='KTsdPYWFRXaFOq1oQpqexxSfemm65A1fDQokriB3nWtMMWRRB6EG6dvwwYZYDdWUvat7yWX4czT0hm0Dd1pop5Dvkke10wqf15T1eO8xypGYa7KjMa09MtM6Fpl'

Configurando as variáveis opcionais
--------------------------------
Utilize a variavel **OAUTH_USER_ATTR_MAP** para mapear os atributos que são recebidos do OAUTH provider para os atributos do modelo de usuário da sua aplicação
::

    OAUTH_USER_ATTR_MAP = {
        "username": "usuario",
        "first_name": "primeiro_nome",
        "last_name": "ultimo_nome"
        }
Incluindo  as views do oauth_client
-------------------------------------

No arquivo ``urls.py`` adicione `oauth_client.urls`

::

    urlpatterns = [
        #...,
        url(r'^', include('oauth_client.urls')),
    ]

