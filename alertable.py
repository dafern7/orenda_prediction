import os
import json
from slack_sdk import WebClient
import sys
import traceback
import ssl
import certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

os.environ['token'] = 'xoxb-1091553225444-3719096455825-O3rESEsI6otLp80pyIOVKuQl'
os.environ['channel'] = 'nyiso-data-alerts'

token = os.environ['token']
channel = os.environ['channel']
client = WebClient(token=os.environ['token'], ssl=ssl_context)

def slack_alert(channel, data):
    function = data['function']
    error = data['error']

    message = f'Check {function} logs for error \n{error}'
    client.chat_postMessage(channel=channel, username=function, text=message)

def alertable(func):
    '''
    Function wrapper that catches all uncaught exceptions and publishes them to 
    an alert channel.
    '''
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            _e = sys.exc_info()
            e = ''.join(traceback.format_exception(*_e))
            fname = func.__name__
            data = {
                'function': fname,
                'error': e
            }
            slack_alert(channel = channel, data = data)
            return 'Error in function execution. Check logs and/or slack channel.', 500

    return wrapper

'''
if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'test_alert.json')
    with open(path, 'r') as file:
        data = json.load(file)
    slack_alert(channel, data)
'''