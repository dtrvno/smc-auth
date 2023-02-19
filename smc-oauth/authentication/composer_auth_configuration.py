import os
dir_file = os.path.dirname(os.path.realpath(__file__))
from authentication.auth_configuration import AuthConfiguration
from smc_utils.smc_jsonutil import save_json
from authorization.scc_user_map import SCCUserMap
class ComposerAuthConfiguration(AuthConfiguration):
    def __init__(self):
        super().__init__()
        self.url="https://172.24.169.66:8887/"
        self.data = {"username": "ADMIN", "password": "111111Aa", "method": "string"}
