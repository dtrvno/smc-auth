import logging

from flask_oidc import OpenIDConnect
import requests

import smc_utils.smc_constants
from smc_utils.smc_exception import SMCException
import json
from authorization.scc_request_path_role_map import SCCRequestPathRoleMap
from authorization.scc_user_map import SCCUserMap
class KeyCloakAuthExecutor:
    def __init__(self,app,auth_configuration):
        self.app=app
        self.configuration=auth_configuration
        self.oidc=None
        self.configuration.init_app(self.app)
        self.admin_token_data=self.get_admin_token()
        self.logger=logging.getLogger(smc_utils.smc_constants.LOGGER_NAME)
    def get_oidc(self):
        if self.oidc is None:
            self.oidc = OpenIDConnect(self.app)
        return self.oidc
    def get_token(self,user,password):
        data = {
            'grant_type': 'password',
            'client_id': self.configuration.client_id,
            'client_secret': self.configuration.client_secret_key,
            'username': user,
            'password': password,
            "scope": "openid"
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        realm = self.configuration.auth_application
        url = "{0}/realms/{1}/protocol/openid-connect/token".format(self.configuration.url,realm)
        response = requests.post(url, data=data, headers=headers)
        if response.status_code > 200:
            message = "Error in getting token: {0}".format(response.text)
            self.logger.error(message)
            raise SMCException(message)
        token_data = response.json()

        self.logger.info("token_data:{0}".format(token_data))
        return token_data

    def get_user_info(self,access_token):
        url = "{0}/realms/{1}/protocol/openid-connect/userinfo".format(self.configuration.url,self.configuration.auth_application)
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        response = requests.request("GET", url, headers=headers, verify=False)
        if response.status_code > 200:
            message = "Error in getting user info"
            raise SMCException(message)
        json_user_info = json.loads(response.text)
        if not self.configuration.is_use_role:
           json_user_info["realm_access"]= SCCUserMap.get_user_roles(json_user_info["sub"])
        self.logger.info("user info:" + json.dumps(json_user_info, indent=4))
        return json_user_info

    def is_user_support_path(self,user_info,path,method):
        roles_obj=user_info["realm_access"]["roles"]
        if SCCRequestPathRoleMap.is_role_supported(roles_obj, path,method):
           return True
        return False

    def get_role_map(self):
        return SCCRequestPathRoleMap.get_role_map()

    def get_admin_token(self):
        data = {
            'grant_type': 'password',
            'client_id': "admin-cli",
            'client_secret': "EXCyVtfc1G8u3ySsqs9jbjkkWFGxx54U",
            'username': 'admin',
            'password': 'admin',
            "scope": "openid"
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        realm = "flask-app"
        url = "{0}/realms/master/protocol/openid-connect/token".format(self.configuration.url)
        response = requests.post(url, data=data, headers=headers)
        if response.status_code > 200:
            message = "Error in getting admin token"
            raise SMCException(message)
        admin_token_data = response.json()
        return admin_token_data
