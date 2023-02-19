from flask_oidc import OpenIDConnect
import requests

import smc_utils.smc_constants
from smc_utils.smc_exception import SMCException
import json
from authorization.scc_request_path_role_map import SCCRequestPathRoleMap
from authorization.scc_user_map import SCCUserMap
import logging
import sys

class ComposerAuthExecutor:
    def __init__(self,app,auth_configuration):
        self.app=app
        self.configuration=auth_configuration
        self.oidc=None
        self.configuration.init_app(self.app)
 #       self.admin_token_data=self.get_admin_token()
        self.logger=logging.getLogger(smc_utils.smc_constants.LOGGER_NAME)

    def get_token(self, user, password):
        login_url = "web/login"
        real_url=self.configuration.url+login_url
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        data = {"username": self.configuration.data.username, "password": self.configuration.data.password,
                "method": self.configuration.data.method}
        response = requests.post(real_url, json=data, headers=headers, verify=False)
        if response.status_code != 200:
            self.logger.error("Wrong code:{0}".format(response.status_code))
            sys.exit(1)
        json_obj = response.json()
        return json_obj