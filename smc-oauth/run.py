from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, jsonify, request, json
from flask_cors import CORS
from flask_oidc import OpenIDConnect
import requests
from keycloak import KeycloakOpenID


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)

# app.config.update({
#     'SECRET_KEY': 'EXCyVtfc1G8u3ySsqs9jbjkkWFGxx54U',
#     'TESTING': True,
#     'DEBUG': True,
#     'OIDC_CLIENT_SECRETS': 'auth.json',
#     'OIDC_ID_TOKEN_COOKIE_SECURE': False,
#     'OIDC_REQUIRE_VERIFIED_EMAIL': False,
#     'OIDC_USER_INFO_ENABLED': True,
#     'OIDC_VALID_ISSUERS': ['http://172.31.32.38:8080/realms/flask-app'],
#     'OIDC_OPENID_REALM': 'http://localhost:5030/oidc_callback',
#     'OIDC_SCOPES': ['openid', 'email', 'profile'],
#     'OIDC_TOKEN_TYPE_HINT': 'access_token',
#     'OIDC_INTROSPECTION_AUTH_METHOD': 'bearer',
#     'OIDC_RESOURCE_CHECK_AUD': True,
#     'OIDC_CLOCK_SKEW': 560
# })

app.config.update({
 #    'SECRET_KEY1': 'u\x91\xcf\xfa\x0c\xb9\x95\xe3t\xba2K\x7f\xfd\xca\xa3\x9f\x90\x88\xb8\xee\xa4\xd6\xe4',
     'SECRET_KEY': 'tcGIsI9LZmfwhYnDrVYdZrTDRhtypath',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'auth.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_VALID_ISSUERS': ['http://172.31.32.38:8080/realms/flask-app'],
    'OIDC_OPENID_REALM1': 'flask-app',
     'OIDC_OPENID_REALM': 'http://localhost:5030/oidc_callback',
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_RESOURCE_CHECK_AUD': True,  # Audience
    'OIDC_CLOCK_SKEW': 560  # iat must be > time.time() - OIDC_CLOCK_SKEW
})
oidc = OpenIDConnect(app)

keycloak_openid = KeycloakOpenID(server_url="http://172.31.32.38:8080/",
                                 client_id="my-client",
                                 realm_name="flask-app",
                                 client_secret_key="tcGIsI9LZmfwhYnDrVYdZrTDRhtypath")
print ("server started")

@app.route("/keycloak/token",methods=["GET"])
def get_token():
    body = request.get_json()
    if body is None:
        message="Data is not provided"
        return custResponse(400, message)
    for field in ['username', 'password']:
        if field not in body:
            return custResponse(400,"authentication error",body)
    data = {
        'grant_type': 'password',
        'client_id': "my-client",
        'client_secret': "EXCyVtfc1G8u3ySsqs9jbjkkWFGxx54U",
        'username': body['username'],
        'password': body['password'],
        "scope":"openid"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    realm="flask-app"
    url="http://172.31.32.38:8080/realms/{0}/protocol/openid-connect/token".format(realm)
    response = requests.post(url, data=data,headers=headers)
    if response.status_code > 200:
        message = "Error in username/password"
        return custResponse(400,message)
    tokens_data = response.json()
    print("token_data:" +json.dumps(tokens_data,indent=4))
    ret = {
        'tokens': {"access_token": tokens_data['access_token'],
                   "refresh_token": tokens_data['refresh_token'],
                   "id_token": tokens_data['id_token']}
    }
    url = "http://172.31.32.38:8080/realms/{0}/protocol/openid-connect/userinfo".format(realm)
    headers = {
        'Authorization': 'Bearer ' + ret["tokens"]["access_token"]
    }
    response = requests.request("GET", url, headers=headers, verify=False)
    if response.status_code > 200:
        message = "Error in getting user info"
        return custResponse(400,message)
    json_user_info=json.loads(response.text)
    print("user info:"+json.dumps(json_user_info,indent=4))
    get_admin_token()
    get_user_role(tokens_data['access_token'],json_user_info["sub"])
    return custResponse(200,"get token",ret)
global admin_token
def get_user_role(access_token,client_id):
    url="http://172.31.32.38:8080/admin/realms/flask-app/users/{0}/role-mappings/realm".format(client_id)
    headers = {
        'Authorization': 'Bearer ' + admin_token
    }
    response = requests.request("GET", url, headers=headers, verify=False)
    if response.status_code > 200:
        message = "Error in getting user roles"
        return
    role_data = response.json()
    print("user role:" + json.dumps(role_data, indent=4))

def get_admin_token():
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
    url = "http://172.31.32.38:8080/realms/master/protocol/openid-connect/token"
    response = requests.post(url, data=data, headers=headers)
    if response.status_code > 200:
        message = "Error in username/password"
        return custResponse(400, message)
    tokens_data = response.json()
    print("admin_token_data:" + json.dumps(tokens_data, indent=4))
    url="http://172.31.32.38:8080/admin/realms/{0}/users".format(realm)
    headers = {
        'Authorization': 'Bearer ' + tokens_data["access_token"]
    }
    response = requests.get(url, data=data, headers=headers)
    if response.status_code > 200:
        message = "Error in  get users"
        return custResponse(400, message)
    users_data=response.json()
    global admin_token
    admin_token=tokens_data["access_token"]
    print("users data:" +json.dumps(users_data, indent=4))

@app.route("/keycloak/version",methods=['GET'],endpoint='get_version')
def get_version():
    return custResponse(200, 'keycloak authentication', {"version":"version 1.0"})

@app.route('/keycloak/api', methods=['POST'])
@oidc.accept_token(require_token=True, scopes_required=['openid'])
def hello_api():
    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})

@app.route('/keycloak/use_login',methods=["GET"])
@oidc.require_login
def protected():
    pass

@oidc.accept_token(require_token=True)
@app.route('/keycloak/use_token',methods=["GET"])
def use_token():
    print("hello")
#    info = oidc.user_getinfo(['preferred_username', 'email', 'sport'])
#    username = info.get('preferred_username')
#    email = info.get('email')
#    sub = info.get('sub')
#    print("""user: %s, email:%s"""%(username, email))

#    token = oidc.get_access_token()
#    return ("""%s"""%token)

    return "hello"

def custResponse(code=404, message="Error: Not Found", data=None):
    message = {
        "status": code,
        "message": message
    }
    if  data:
        if isinstance(data, str):
           resp = jsonify(json.loads(data))
        else:
            resp = jsonify(data)
    else:
        resp = jsonify(message)
    resp.status_code = code
    return resp

if __name__ == '__main__':
   port=5030
   app.run(host='0.0.0.0',port=port, debug=True)
