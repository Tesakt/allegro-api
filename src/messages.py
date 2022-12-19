import requests
import json



class Messages:
    access_token = None
    notice = "Dziękujemy za kontakt. W tej chwili niestety nie jesteśmy w stanie odpowiedzieć na Państwa pytanie od ręki. Osoba odpowiedzialna za obsługę klientów jest obecnie zajęta innymi sprawami, ale postaramy się odpisać jak najszybciej. Prosimy o cierpliwość. W razie pilnej potrzeby, prosimy o kontakt pod numerem infolinii. Dziękujemy za zrozumienie i pozdrawiamy serdecznie."
    THREADS_URL = "https://api.allegro.pl/messaging/threads"
    MESSAGES_URL = "https://api.allegro.pl/messaging/messages"
    
    def __init__(self, token):
        self.access_token = token
        
    def get_list_of_threads(self):
        try:
            headers = {'Accept': 'application/vnd.allegro.public.v1+json', 'Authorization': 'Bearer ' + self.access_token}
            api_call_response = requests.get(self.THREADS_URL, headers=headers, verify=False)
            # Save threads to file
            with open('threads.json', 'w') as outfile:
                json.dump(api_call_response.text, outfile)
            return
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
    
    def new_message(self, thread_id):
        try:
            headers = {'Accept': 'application/vnd.allegro.public.v1+json', 'Authorization': 'Bearer ' + self.access_token}
            data = {'message': self.notice}
            api_call_response = requests.post(self.MESSAGES_URL + '/' + thread_id, headers=headers, data=data, verify=False)
            return api_call_response
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        
    def check_new_messages(self):
        # Check if there is file named threads.json
        try:
            with open('threads.json', 'r') as threads_file:
                threads = json.load(threads_file)
            threads = json.loads(threads)
            threads = threads['threads']
            for thread in threads:
                if thread['read'] == 'false':
                    response = self.new_message(self.access_token, thread['id'], self.notice)
                    print(response.text)
        except IOError:
            print("File not accessible")
            return