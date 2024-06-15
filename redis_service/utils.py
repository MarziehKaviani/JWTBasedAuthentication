import json

import redis
from common.variables import TRY_AGAIN_LATER
from JWTBasedAuthentication.settings import REDIS_CLIENT


def check_redis_health():
    try:
        response = REDIS_CLIENT.ping()
        if response:
            return True
        else:
            return False
    except redis.ConnectionError as e:
        return False
    except redis.RedisError as e:
        return False


class RedisStore:
    """
    Utility class for interacting with Redis cache.

    Methods:
    - set(self, key: str, value: Any, expires_in_minutes: int) -> None:
        Set a key-value pair in the Redis cache with an expiration time.
    - get(self, key: str) -> Any:
        Retrieve the value associated with the given key from the Redis cache.
    - remove(self, key: str) -> None:
        Remove the key-value pair associated with the given key from the Redis cache.
    """

    def __init__(self) -> None:
        self.redis_client = REDIS_CLIENT

    def set(self, key, value, expires_in_minutes):
        """
        Set a key-value pair in the Redis cache with an expiration time.

        Parameters:
        - key (str): The key to store the value under in the Redis cache.
        - value (Any): The value to be stored in the Redis cache.
        - expires_in_minutes (int): The expiration time for the key-value pair in minutes.
        """
        if isinstance(value, dict):
            value = json.dumps(value)
        
        self.redis_client.set(key, value)
        self.redis_client.expire(key, expires_in_minutes * 60)

    def get(self, key):
        """
        Retrieve the value associated with the given key from the Redis cache.

        Parameters:
        - key (str): The key whose associated value is to be retrieved from the Redis cache.

        Returns:
        - Any: The value associated with the given key, or None if the key does not exist.
        """
        val: str = self.redis_client.get(key)
        if val:
            if val.startswith("{") and val.endswith("}"):
                val = json.loads(val)
        return val

    def remove(self, key):
        """
        Remove the key-value pair associated with the given key from the Redis cache.

        Parameters:
        - key (str): The key of the key-value pair to be removed from the Redis cache.
        """
        self.redis_client.delete(key)

    def flush(self):
        self.redis_client.flushdb()