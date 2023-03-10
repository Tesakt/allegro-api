from src.access import Api
from src.scheduler import Scheduler
import os

def main():
    # Get CLIENT_ID and CLIENT_SECRET from environment variables
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

    # Create API object
    API = Api(CLIENT_ID, CLIENT_SECRET)

    update_period = 60
    
    while True:
        # Validate access token
        if API.check_token() == False:
            result = API.get_code()
            API.await_for_access_token(int(result['interval']), result['device_code'])

        # Run scheduler for messages
        scheduler = Scheduler(update_period, API.access_token)
        scheduler.main()        
        
if __name__ == '__main__':
    main()