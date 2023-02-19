from flask_oidc import OpenIDConnect
import requests
from smc_utils.smc_exception import SMCException
from authentication.empty_oidc import EmptyOidc
class EmptyAuthExecutor:
    def __init__(self,app):
        pass
    def get_oidc(self):
        return EmptyOidc()
    def get_token(self,user,password):
        data= {
            "access_token":"empty_token",
            "scope": "empty",
            "session_state": "empty",
            "token_type": "Bearer"
        }
        return data

    def get_user_info(self, access_token):
        data = {"user_info":"empty"}
        return data

    def is_user_support_path(self,user_info,path,method):
        return True
