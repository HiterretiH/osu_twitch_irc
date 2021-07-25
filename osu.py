import socket
import requests
import time
import json
from threading import Timer


class OsuBot:
    def __init__(self, name: str, password: str):
        self.host = "irc.ppy.sh"
        self.port = 6667
        self.name = name
        self.password = password
        self.reconnect = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._msg_max = 9  # 10 (-1) messages per 5 seconds
        self._msg_timeout = 5
        self._msg_cnt = 0

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.send("PASS " + self.password)
        self.send("NICK " + self.name)
        self.send(f"USER {self.name} {self.host} 1 :{self.name}")
        print("Conncected to Bancho")

    def close(self):
        self.sock.close()

    def send(self, text: str):
        if self._msg_cnt >= self._msg_max:
            Timer(5, self.send, [text]).start()
            return
        self._msg_cnt += 1
        self.sock.send((text + '\n').encode())
        Timer(self._msg_timeout, self._msg_cnt_decrement_).start()

    def _msg_cnt_decrement_(self):
        self._msg_cnt -= 1


class OsuApi:
    def __init__(self, client_id: str, client_secret: str):
        self.url = "https://osu.ppy.sh/api/v2"
        self.id = client_id
        self.secret = client_secret
        self.max_time = 0
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def get_token(self):
        data = {
            'client_id': self.id,
            'client_secret': self.secret,
            'grant_type': 'client_credentials',
            'scope': 'public'
        }
        res = requests.post("https://osu.ppy.sh/oauth/token", data=data).json()
        self.headers.update({ "Authorization": f"Bearer {res.get('access_token')}" })
        self.max_time = int(time.time()) + int(res.get('expires_in')) - 100
        print("Got new osu api token")
        return res

    def get(self, api: str, data=dict()):
        if time.time() >= self.max_time:
            self.get_token()
        return requests.get(self.url + api, params=data, headers=self.headers).json()

    def post(self, api: str, data=dict(), body=dict()):
        body = json.dumps(body)
        if time.time() >= self.max_time:
            self.get_token()
        return requests.post(self.url + api, params=data, json=body, headers=self.headers).json()

    def get_beatmap(self, map_id: str):
        return self.get("/beatmaps/" + map_id)
