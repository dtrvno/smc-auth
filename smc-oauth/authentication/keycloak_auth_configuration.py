import os
dir_file = os.path.dirname(os.path.realpath(__file__))
from authentication.auth_configuration import AuthConfiguration
from smc_utils.smc_jsonutil import save_json
from authorization.scc_user_map import SCCUserMap
class KeyCloakAuthConfiguration(AuthConfiguration):

    def __init__(self):
        super().__init__()
        self.url="http://172.31.32.38:8080/"
        self.url17 = "http://172.31.32.38:8081/"
        self.url20 = "http://172.31.32.38:8080/"
        self.admin_user="admin"
        self.admin_password="admin"
        self.auth_application="flask-app"
        self.auth_application_port=5030   # in our case it is orchestrator port
        self.client_id="my-client"
        self.client_secret_key="tcGIsI9LZmfwhYnDrVYdZrTDRhtypath"
        self.client_secret_key17 = "6YfG8z0UouOabwtsD2C56xOeB13uesbt"
        self.client_secret_key20 = "tcGIsI9LZmfwhYnDrVYdZrTDRhtypath"
        self.init_configuration()
        self.is_use_role=True
        if not self.is_use_role:
           self.init_roles()

    def init_roles(self):
        sub="be025355-a77c-44af-8b1b-fd50de26ede1"
        SCCUserMap.add_role_to_user(sub,"admin_role")
        SCCUserMap.add_role_to_user(sub, "manager_role")
        sub="de44e35c-d071-44d6-af4e-2ffd5ac5cf04"
        SCCUserMap.add_role_to_user(sub, "regular_role")
        SCCUserMap.add_role_to_user(sub, "developer_role")

    def init_configuration(self):
        auth_conf={
            "web": {
                "issuer": "{0}/realms/{1}".format(self.url,self.auth_application),
                "auth_uri": "{0}/realms/{1}/protocol/openid-connect/auth".format(self.url,self.auth_application),
                "client_id": self.client_id,
                "client_secret": self.client_secret_key,
                "redirect_uris": [
                    "http://localhost:{0}/*".format(self.auth_application_port)
                ],
                "userinfo_uri": "{0}/realms/{1}/protocol/openid-connect/userinfo".format(self.url,self.auth_application),
                "token_uri": "{0}/realms/{1}/protocol/openid-connect/token".format(self.url,self.auth_application),
                "token_introspection_uri": "{0}/realms/{1}/protocol/openid-connect/token/introspect".format(self.url,self.auth_application),
                "use-resource-role-mappings": True
            }
        }
        auth_file_path=os.path.join(dir_file,"auth.conf")
        save_json(auth_file_path,auth_conf)

    def init_app(self,app):
        app.config.update({
            'SECRET_KEY': self.client_secret_key,
            'TESTING': True,
            'DEBUG': True,
            'OIDC_CLIENT_SECRETS': 'auth.json',
            'OIDC_ID_TOKEN_COOKIE_SECURE': False,
            'OIDC_REQUIRE_VERIFIED_EMAIL': False,
            'OIDC_USER_INFO_ENABLED': True,
            'OIDC_VALID_ISSUERS': ['{0}/realms/{1}'.format(self.url,self.auth_application)],
            'OIDC_OPENID_REALM': 'http://localhost:{0}/oidc_callback'.format(self.auth_application_port),
            'OIDC_OPENID_REALM1': 'flask-app',
            'OIDC_SCOPES': ['openid', 'email', 'profile'],
            'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
            'OIDC_RESOURCE_CHECK_AUD': True,  # Audience
            'OIDC_TOKEN_TYPE_HINT': 'access_token',
            'OIDC_CLOCK_SKEW': 560  # iat must be > time.time() - OIDC_CLOCK_SKEW
        })

