from requests import RequestException

import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import http
from codecs import encode
import ssl
import sys

class AuthClient:
    def __init__(self):
        self.token=None
    def print_out(self, message):
        print(message)
    def __init__(self):
        pass
    def get_roles_map(self):
        url = "http://localhost:5030/v1/roles_map".format()
        headers = {
            'Accept': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, verify=False)
        json_obj = json.loads(response.text)
        print("roles_data:" + json.dumps(json_obj, indent=4))

    def get_token(self,user,password):
        url = "http://localhost:5030/v1/token".format()
        headers = {
            'Accept': 'application/json'
        }
        payload = {"username":user,"password":password}

        response = requests.request("GET", url, headers=headers, json=payload,verify=False)
        if response.status_code !=200:
            print("token_data:" + response.text)
            sys.exit(1)
        json_obj=json.loads(response.text)

        print("json_data:" +json.dumps(json_obj, indent=4))
        access_token=json_obj["token_data"]["access_token"]

        headers={
            'Authorization': 'Bearer ' + access_token
        }
        url = "http://localhost:5030/v1/execute1"
        response = requests.request("GET", url, headers=headers, verify=False)
        json_obj = json.loads(response.text)
        print("user_data:" + json.dumps(json_obj, indent=4))

        url = "http://localhost:5030/v1/execute2"
        response = requests.request("GET", url, headers=headers, verify=False)
        json_obj = json.loads(response.text)
        print("user_data:" + json.dumps(json_obj, indent=4))



if __name__ == '__main__':
    cloud = AuthClient()
    cloud.get_roles_map()
    cloud.get_token("dima","test123")
    cloud.get_token("jim", "test123")


