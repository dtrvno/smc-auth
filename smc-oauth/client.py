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

    def get_token(self):
        url = "http://localhost:5030/keycloak/token".format()
        headers = {
            'Accept': 'application/json'
        }
        # payload = {"username":"dima","password":"irinadima"}
        payload = {


            'username': "dima",
            'password': "irinadima",

        }

        response = requests.request("GET", url, headers=headers, json=payload,verify=False)
        json_obj=json.loads(response.text)
        self.token=json_obj["tokens"]["id_token"]
        print(self.token)
        headers={
            'Authorization': 'Bearer ' + self.token
        }
        url = "http://localhost:5030/keycloak/use_token"
        response = requests.request("GET", url, headers=headers, verify=False)
        print ("before use login")
        url = "http://localhost:5030/keycloak/use_login"
        response = requests.request("GET", url, headers=headers, verify=False)


if __name__ == '__main__':
    cloud = AuthClient()
    cloud.get_token()


