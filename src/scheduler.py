from src.messages import Messages
from datetime import datetime
import time

class Scheduler:
    
    def __init__(self, update_period, access_token):
        self.update_period = update_period
        self.Message_manager = Messages(access_token)

    def check_time(self):
        now = datetime.now()
        if now.weekday() == 5:      # Saturday
            return now.hour <= 8 or now.hour >= 13
        elif now.weekday() == 6:    # Sunday
            return True
        else:                       # Monday - Friday
            return now.hour <= 8 or now.hour >= 17

    def main(self):
        if self.check_time():
            self.Message_manager.get_list_of_threads()
            self.Message_manager.check_new_messages()
        time.sleep(self.update_period)