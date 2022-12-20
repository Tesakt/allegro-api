import requests
import json
import time

class Api:
    CLIENT_ID = None
    CLIENT_SECRET = None
    CODE_URL = "https://allegro.pl/auth/oauth/device"
    TOKEN_URL = "https://allegro.pl/auth/oauth/token"
    buffer_time = 3600
    access_token = None
    
    def __init__(self, client_id, client_secret):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
    
    def get_code(self):
        try:
            payload = {
                'client_id': self.CLIENT_ID
            }
            headers = {
                'Content-type': 'application/x-www-form-urlencoded'
            }
            api_call_response = requests.post(self.CODE_URL, auth=(self.CLIENT_ID, self.CLIENT_SECRET), headers=headers, data=payload, verify=False)
            result = json.loads(api_call_response.text)
            print(result['verification_uri_complete'])
            return result
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
    def check_token(self):
        try:
            with open('token.json', 'r') as token_file:
                token = json.load(token_file)
            self.access_token = token['access_token']
            if time.time() - token['current_time'] - self.buffer_time > token['expires_in']:
                return False
            return True
        except IOError:
            return False
    
    def get_access_token(self, device_code):
        try:
            headers = {
                'Content-type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code', 
                'device_code': device_code
            }
            api_call_response = requests.post(self.TOKEN_URL, auth=(self.CLIENT_ID, self.CLIENT_SECRET), headers=headers, data=data, verify=False)
            return api_call_response
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    def await_for_access_token(self, interval, device_code):
        while True:
            time.sleep(interval)
            result_access_token = self.get_access_token(device_code)
            token = json.loads(result_access_token.text)
            if result_access_token.status_code == 400:
                if token['error'] == 'slow_down':
                    interval += interval
                if token['error'] == 'access_denied':
                    break
            else:
                self.access_token = token['access_token']
                token['current_time'] = time.time()
                with open('token.json', 'w') as outfile:
                    # add current time to access token file
                    json.dump(token, outfile)
                return