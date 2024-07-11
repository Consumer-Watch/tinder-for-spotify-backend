import firebase_admin
from firebase_admin import credentials


app_options = {'projectId': 'sonder-63ac2'}
default_app = firebase_admin.initialize_app(options=app_options)