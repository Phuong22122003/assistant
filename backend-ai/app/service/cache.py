from app.core import service
import redis

@service
class Cache:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        pass
    def set(self,key,value):
        self.r.set(key,value)
    def get(self,key):
        return self.r.get(key)