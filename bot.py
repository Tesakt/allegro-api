from src.access import Api
from src.messages import Messages
from datetime import datetime
import time
import os

# Function that checks if it is time to run the script
def check_time():
    now = datetime.now()
    if now.weekday() == 5:      # Saturday
        return now.hour <= 8 or now.hour >= 13
    elif now.weekday() == 6:    # Sunday
        return True
    else:                       # Monday - Friday
        return now.hour <= 8 or now.hour >= 17
    
    
def main():
    # Get CLIENT_ID and CLIENT_SECRET from environment variables
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

    # Create API object
    API = Api(CLIENT_ID, CLIENT_SECRET)

    # Initiate device authorization
    result = API.get_code()
    # Need to change this to GUI
    print(result['verification_uri_complete'])
    API.await_for_access_token(int(result['interval']), result['device_code'])

    # Set update period in seconds
    update_period = 60
    
    # Create manager for messages
    Message_manager = Messages(API.access_token)
    while True:
        if check_time():
            Message_manager.get_list_of_threads()
            Message_manager.check_new_messages()
        time.sleep(update_period)
        
        
if __name__ == '__main__':
    main()