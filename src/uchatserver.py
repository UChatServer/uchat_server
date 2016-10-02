#! python

import os

from user import User

class UChatServer:
    def __init__(self, app_key = None, app_secret = None):
        if app_key is None:
            app_key = os.environ.get('APP_KEY', '')
        if app_secret is None:
            app_secret = os.environ.get('APP_SECRET', '')
        self.User = User(app_key, app_secret)
 
