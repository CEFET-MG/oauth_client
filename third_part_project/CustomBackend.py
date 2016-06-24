from oauth_client.OauthBackend import OauthBackend


class CustomBackend(OauthBackend):

    def user_is_valid(self, oauth_response):

        return oauth_response['username']=='higoramp_dri'

    def post_create(self, user):

        pass