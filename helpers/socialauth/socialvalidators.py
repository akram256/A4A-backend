import facebook
from google.auth.transport import requests
from google.oauth2 import id_token
import twitter
from decouple import config



class FacebookAuthHandler:
    """
    Class to get Facebook user information and return it
    
    """

    @staticmethod
    def validate(auth_token):
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            # print(graph)
            profile = graph.request('/me?fields=id,name,email')
            print(profile)
            return profile
        except Exception:
            message = "The token is invalid or expired."
            return message


class GoogleAuthHandler:
    """Class to handle Google user info"""

    @staticmethod
    def validate(auth_token):
        """
        Gets and validates Google the user info from the auth token
        """
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())
            if idinfo['iss'] not in ['accounts.google.com',
                                     'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            return idinfo
        except ValueError:
            return "The token is either invalid or has expired"

class TwitterAuthHandler:
    """
    Class to handle twitter auth tokens
    by splitting the two tokens and validating them
    """
    @staticmethod
    def split_twitter_auth_tokens(tokens):
        """
        Splits the token sent in the request into two:
        access token and access_token_secret
        """
        auth_tokens = tokens.split(' ')
        if len(auth_tokens) < 2:
            return 'invalid token'
        access_token = auth_tokens[0]
        access_token_secret = auth_tokens[1]
        return access_token, access_token_secret

    @staticmethod
    def validate(tokens):
        """
        Validates twitter auth and returns user info as a dict
        """
        access_token_key, access_token_secret = TwitterAuthHandler\
            .split_twitter_auth_tokens(tokens)
        try:
            consumer_api_key = config('TWITTER_APP_CONSUMER_API_KEY')
            consumer_api_secret_key = config(
                'TWITTER_APP_CONSUMER_API_SECRET_KEY'
            )

            api = twitter.Api(
                consumer_key=consumer_api_key,
                consumer_secret=consumer_api_secret_key,
                access_token_key=access_token_key,
                access_token_secret=access_token_secret
            )

            user_profile_info = api.VerifyCredentials(include_email=True)
            return user_profile_info.__dict__
        except Exception:
            message = "The token is invalid or expired."
            return message


