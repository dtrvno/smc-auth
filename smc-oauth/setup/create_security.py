import json
import requests
from keycloak import KeycloakAdmin
class CreateSecurity:

    def __init__(self):
        pass
    def get_admin_token(self):
        data = {
        'grant_type': 'password',
        'client_id': "admin-cli",
        'username': 'admin',
        'password': 'admin'

        }
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = "http://172.31.32.38:8080/realms/master/protocol/openid-connect/token"
        response = requests.post(url, data=data)
        self.admin_tokens_data = response.json()
        if response.status_code > 200:
           message="Error in getting token:{0}".format(json.dumps(self.admin_tokens_data,indent=4))
           print(message)
        print("admin_token_data:"+json.dumps(self.admin_tokens_data,indent=4))
        print("admin_token:" + self.admin_tokens_data["access_token"])
        
    def delete_realm(self,realm):
        url = 'http://172.31.32.38:8080/admin/realms/{0}'.format(realm)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.admin_tokens_data["access_token"]
        }
        x = requests.delete(url, headers=headers)
        print("deleted realm. status:{0}".format(x.status_code))

    def create_realm(self, realm):
        false=False
        true=True
        url = 'http://172.31.32.38:8080/admin/realms/'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.admin_tokens_data["access_token"]
        }
        data={

           "realm": "demo",
           "enabled": True
        }

        data=open('realm_test.json','rb')
        x = requests.post(url, headers=headers, data=data)
        if x.status_code==201:
           print("realm {0} created ".format(realm))
        return x.content

    def create_client(self, realm,client):
        url = 'http://172.31.32.38:8080/admin/realms/{0}/clients'.format(realm)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.admin_tokens_data["access_token"]
        }
        data = {

            "clientId": client,
            "enabled": True
        }
        data = open('clients.json', 'rb')
        x = requests.post(url, headers=headers,data=data)
        print("created client. status:{0}".format(x.status_code))
    def list_users(self):
        print ("admin_token_list_users:"+ self.admin_tokens_data["access_token"])
        url = 'http://172.31.32.38:8080/admin/realms/flask-app/users'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.admin_tokens_data["access_token"]
        }
        response = requests.get(url, headers=headers,data={})
        users_obj=response.json()
        print("list_users:" + json.dumps(users_obj, indent=4))

    def create_user(self,realm):
        true=True
        false=False
        url = "http://172.31.32.38:8080/admin/realms/{0}/users".format(realm)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.admin_tokens_data["access_token"]
        }

        data = open('users.json', 'rb')
        response = requests.post(url, headers=headers,data=data)
        print("create_user:{0}".format(response.status_code))



if __name__ == '__main__':
   sec=CreateSecurity()
   sec.get_admin_token()
   sec.delete_realm("demo")
   sec.create_realm("demo")
   sec.create_client("demo","my-client")
   sec.list_users()
   sec.create_user("demo")
