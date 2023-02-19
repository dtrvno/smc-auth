import os
dir_file = os.path.dirname(os.path.realpath(__file__))
from authentication.auth_configuration import AuthConfiguration
from smc_utils.smc_jsonutil import save_json
class EmptyAuthConfiguration(AuthConfiguration):
      def __init__(self):
          super().__init__()