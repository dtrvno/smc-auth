import logging

from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, jsonify, request, json
from flask_cors import CORS
from flask_oidc import OpenIDConnect
import requests
from keycloak import KeycloakOpenID

import smc_utils.smc_constants
from authentication.auth_factory import AuthFactory
from authentication.auth_executor import AuthExecutor
from smc_utils.smc_exception import SMCException
from smc_utils.logging_configuration import LoggingConfiguration

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)
auth_provider="keycloak"
#auth_provider=None
auth_config=AuthFactory.get_configuration_instance(auth_provider)
auth_executor=AuthFactory.get_executor_instance(app,auth_configuration=auth_config,auth_name=auth_provider)
oidc=auth_executor.get_oidc()
LoggingConfiguration()
logger=logging.getLogger(smc_utils.smc_constants.LOGGER_NAME)

print ("server started")

@app.route("/v1/token",methods=["GET"])
def get_token():
    body = request.get_json()
    if body is None:
        message="Data is not provided"
        return custResponse(400, message)
    for field in ['username', 'password']:
        if field not in body:
            return custResponse(400,"authentication error",body)
    try:
       json_token=auth_executor.get_token(body["username"],body["password"])
       user_info=auth_executor.get_user_info(json_token["access_token"])
       return_data={"token_data":json_token,"user_info":user_info}
    except SMCException as e:
       message=e.message;
       return custResponse(500, message)
    return custResponse(200,"get token",return_data)

@app.route("/v1/roles_map", methods=["GET"])
def get_role_map():
    role_map= auth_executor.get_role_map()
    return custResponse(200, "method get role map", role_map)

@app.route("/v1/execute1", methods=["GET"])
@oidc.accept_token(require_token=True)
def execute1():
    logger.info("token accepted")
    full_token=request.headers["Authorization"]
    access_token=full_token[len("Bearer"):].strip()
    user_info=auth_executor.get_user_info(access_token)
    if auth_executor.is_user_support_path(user_info,request.path,request.method):
       logger.info("method is supported. we are going to call it")
       return custResponse(200, "method execute1", {"status":"success"})
    else:
       message="Path {0} is not supported for that user".format(request.path)
       logger.error(message)
       return custResponse(500, message)

@app.route("/v1/execute2",methods=["GET"])
@oidc.accept_token(require_token=True)
def execute2():
    logger.info("token accepted")
    full_token = request.headers["Authorization"]
    access_token = full_token[len("Bearer"):].strip()
    user_info = auth_executor.get_user_info(access_token)
    if auth_executor.is_user_support_path(user_info, request.path,request.method):
        logger.info("method is supported. we are going to call it")
        return custResponse(200, "method execute2", {"status": "success"})
    else:
        message = "Path is not supported for that user"
        logger.error(message)
        return custResponse(500, message)



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
