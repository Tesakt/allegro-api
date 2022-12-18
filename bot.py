from src.api import Api
from src.messages import Messages
import os

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

# Create manager for messages
Message_manager = Messages(API.access_token)
Message_manager.get_list_of_threads()
Message_manager.check_new_messages()