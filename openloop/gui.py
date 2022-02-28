# Classes for Statistics and Management of web.py

import socket, requests
from openloop.version import version, code, device


class NavElement:
    def __init__(self, name, href):
        self.name = name
        self.href = href

class Version:
    def __init__(self):
        self.version = version
        self.code = code
        self.device = device

class System:
    def __init__(self) -> None:
        self.hostname = socket.gethostname()   
        self.ip = socket.gethostbyname(self.hostname) 
        