import requests
import json
import time

class Messages:
    access_token = None
    notice = "Dziękujemy za kontakt. W tej chwili niestety nie jesteśmy w stanie odpowiedzieć na Państwa pytanie od ręki. Osoba odpowiedzialna za obsługę klientów jest obecnie zajęta innymi sprawami, ale postaramy się odpisać jak najszybciej. Prosimy o cierpliwość. W razie pilnej potrzeby, prosimy o kontakt pod numerem infolinii. Dziękujemy za zrozumienie i pozdrawiamy serdecznie."
    THREADS_URL = "https://api.allegro.pl/messaging/threads/"
    
    def __init__(self, token):
        self.access_token = token
        
    def get_list_of_threads(self):
        try:
            headers = {
                'Accept': 'application/vnd.allegro.public.v1+json', 
                'Authorization': 'Bearer ' + self.access_token
            }
            api_call_response = requests.get(self.THREADS_URL, headers=headers, verify=False)
            api_call_response = json.loads(api_call_response.text)
            # Save threads to file
            with open('threads.json', 'w') as outfile:
                json.dump(api_call_response, outfile)
            return
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
    
    def new_message(self, thread_id):
        try:
            headers = {
                'Accept': 'application/vnd.allegro.public.v1+json', 
                'Authorization': 'Bearer ' + self.access_token, 
                'Content-Type': 'application/vnd.allegro.public.v1+json'
            }
            data = {"text": self.notice}
            api_call_response = requests.post(self.THREADS_URL + thread_id + '/messages', headers=headers, json=data, verify=False)
            return api_call_response
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
    def check_new_messages(self):
        # Check if there is file named threads.json
        try:
            with open('threads.json', 'r') as threads_file:
                threads = json.load(threads_file)
            threads = threads['threads']
            for thread in threads:
                if thread['read'] == False:
                    response = self.new_message(thread['id'])
                    time.sleep(1)
                    print(response)
        except IOError:
            print("File not accessible")
            return