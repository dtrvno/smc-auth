from authentication.keycloak_auth_configuration import KeyCloakAuthConfiguration
from authentication.keycloak_auth_executor import KeyCloakAuthExecutor
from authentication.empty_auth_configuration import EmptyAuthConfiguration
from authentication .empty_auth_executor import EmptyAuthExecutor
from smc_utils.smc_exception import SMCException

class AuthFactory:
    @staticmethod
    def get_configuration_instance(auth_name=None):
        if auth_name=="keycloak":
           return  KeyCloakAuthConfiguration()
        if auth_name is None:
           return  EmptyAuthConfiguration()
        if auth_name=="composer":
           return EmptyAuthConfiguration()
        message="Provider {0} is not supported".format(auth_name)
        raise SMCException(message)

    @staticmethod
    def get_executor_instance(app,auth_configuration=None,auth_name=None):
        if auth_name=="keycloak":
            return KeyCloakAuthExecutor(app, auth_configuration=auth_configuration)
        if auth_name is None:
            return EmptyAuthExecutor(app)
        message = "Provider {0} is not supported".format(auth_name)
        raise SMCException(message)
