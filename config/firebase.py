import firebase_admin
from firebase_admin import credentials
from os import getenv


app_options = {'projectId': 'sonder-63ac2'}

def get_credentials():
    if getenv("GCP_PRIVATE_KEY"):
        return {
            "credentials": {
                "client_email": getenv("GCP_SERVICE_ACCOUNT_EMAIL"),
                "private_key": getenv("GCP_PRIVATE_KEY"),
            },
            'projectId': 'sonder-63ac2'
        }
    else:
        return None
    
default_app = firebase_admin.initialize_app(credential=None)