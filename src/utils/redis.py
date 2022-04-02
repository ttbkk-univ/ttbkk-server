import redis
import env


class Redis:
    _client = None

    @staticmethod
    def get_client():
        if Redis._client:
            return Redis._client
        Redis._client = redis.Redis(host=env.REDIS_HOST, port=env.REDIS_PORT)
        return Redis._client

