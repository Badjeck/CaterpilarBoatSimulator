import time
import pickle
import socket

class Network:
    def __init__(self, ip, port):
        self.client = socket.socket()
        self.ip = str(ip)
        self.port = port
        self.addr = (self.ip, self.port)
        self.pos = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
        except socket.error as e:
            print(str(e))
            
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)

    def recv(self, lenght):
        return pickle.loads(self.client.recv(lenght))