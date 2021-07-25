import socket
from threading import Timer


class TwitchBot:
    def __init__(self, name: str, password: str, channel: str):
        self.host = 'irc.chat.twitch.tv'
        self.port = 6667
        self.name = name.lower()
        self.password = password
        self.channel = channel
        self.reconnect = 0
        self.sock = socket.socket()
        self._msg_max = 19  # 20 (-1) messages per 30 seconds
        self._msg_timeout = 30
        self._msg_cnt = 0

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.send("PASS " + self.password)
        self.send("NICK " + self.name)
        self.send("JOIN " + self.channel)
        print("Conncected to twitch")

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

    def receive(self, size: int):
        return self.sock.recv(size)

    def reply(self, name: str, msg: str):
        self.send(f"PRIVMSG {self.channel} :@{name}, {msg}")
        print(f"twitchbot: @{name}, {msg}")
