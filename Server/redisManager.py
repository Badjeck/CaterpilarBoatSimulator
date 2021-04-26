import redis

class RedisManager:

    def __init__(self):
        self.ip = 'localhost'
        self.port = 6379
        self.r = redis.Redis(host=self.ip, port=self.port)
    
    def send(self, id, position):
        self.r.set(f'{id}:pos', position)

    def get(self, id):
        return self.r.get(f'{id}:pos').decode()

    def test(self):
        print(self.r.ping())