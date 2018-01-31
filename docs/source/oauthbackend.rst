OAuthBackend
===================================


Customizando o backend
##############################

Caso precise alterar o fluxo de autenticação padrão do módulo é possível herdando a classe ``OauthBackend``

::

    class CustomBackend(OauthBackend):
        #.....

A classe ``OauthBackend`` possui dois métodos que podem ser utilizados para uma maior flexibilidade do módulo. São eles: ``user_is_valid`` e ``post_create``

Validando o usuário antes de logar no sistema
-------------------------------------

Algumas aplicações podem precisar de validar o usuário autenticado no servidor OAuth antes de realizar o login. Pensando nisso, foi criado o método ``user_is_valid``, onde podem ser feitas validações de acordo com a resposta do Servidor Oauth, antes mesmo de logar o usuário na aplicação cliente.

O método deve retornar **True** caso o usuário possa logar no sistema e **False** caso contrário

Ps. Utilize a lista **errors** para enviar as mensagens de erro que serão mostradas ao usuário.
::

    class CustomBackend(OauthBackend):

        def user_is_valid(self, oauth_response, errors):

            return oauth_response['username']=='higoramp_dri'


Executando ações após logar no sistema
------------------------------------
Outra possibilidade de customização se dá através do método ``post_create``, que é chamado após o usuário logar no sistema pela primeira vez. Esse método é muito útil caso precisa criar uma classe Profile para o seu usuário, com atributos extras ao modelo padrão

::

    class CustomBackend(OauthBackend):

        def post_create(self, user):
            ProfileUser.create(user=user, tipo_vinculo=user.oauth_response['vinculos'][0]['tipo_vinculo'])
