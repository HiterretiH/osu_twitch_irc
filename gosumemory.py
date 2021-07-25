import requests
from threading import Timer

timeout = 5
requested = False
data = dict()

def get_data():
    global data, requested
    if not requested:
        data = requests.get("http://localhost:24050/json").json()
        requested = True
        Timer(timeout, __unset_requested__).start()
    return data

def __unset_requested__():
    global requested
    requested = False
