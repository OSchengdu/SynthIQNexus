import redis

class RedisManager:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379)

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)
