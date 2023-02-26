import redis


class RedisHelper:
    def __init__(self):
        host = "127.0.0.1"
        port = 6379
        db = 5
        self.redis = redis.Redis(host=host, port=port, db=db, password="s")

    def set(self, key, value):
        return self.redis.set(key, value)

    def set_key_with_timeout(self, key, value, timeout=60):
        self.redis.setex(key, timeout, value)

    def get(self, key):
        return self.redis.get(key)

    def delete(self, key):
        return self.redis.delete(key)

    def exists(self, key):
        return self.redis.exists(key)

    def expire(self, key, seconds):
        return self.redis.expire(key, seconds)

    def ttl__(self,key):
        return self.redis.ttl(key)


# if __name__ == '__main__':
#     res = RedisHelper().set_key_with_timeout("sukiyou", "sukiyou")
#     # res = RedisHelper().get('sukiyou')
#     # print(res)
#     res = RedisHelper().exists('sukiyou')
#     print(res)
#     if res:
#         print( RedisHelper().expire())
#         print(1)
#     else:
#         print(0)
