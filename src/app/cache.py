import redis
import environ

env = environ.Env()


class Cache:
    def __init__(self):
        self.r = redis.Redis(host=env('REDIS'), port=env('REDISPORT'))

    def set(self, key="", value=""):
        self.r.set(f"{key}", value)

    def get(self, key="", tp=str):
        raw_res = self.r.get(f"{key}")
        return tp(raw_res.decode("utf-8")) if raw_res is not None else None
