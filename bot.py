from src.api import Api
import os

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

API = Api(CLIENT_ID, CLIENT_SECRET)