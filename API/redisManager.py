import redis

class RedisManager:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.r = redis.Redis(host=self.ip, port=self.port)
    
    def send(self, id, position):
        self.r.set(id, position)

    def get(self, id):
        return self.r.get(id)
        

red = RedisManager('127.0.0.1', 6379)
red.send('lalala', 'test')
print(red.get('lalala'))