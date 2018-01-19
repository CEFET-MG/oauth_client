import base64


def get_basic_auth_header(client_id, client_secret):
        """
        Return a dict containg the correct headers to set to make HTTP Basic Auth request
        """
        user_pass = '{0}:{1}'.format(client_id, client_secret)
        auth_string = base64.b64encode(user_pass.encode('utf-8'))
        auth_headers = {
            'Authorization': 'Basic ' + auth_string.decode("utf-8"),
        }

        return auth_headers