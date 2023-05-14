import redis
from redis import Redis


class RedisError(Exception):
    """Custom exception for Redis errors."""


class RedisClient:
    """
    A Redis client wrapper class for simplified interaction with Redis.
    """

    def __init__(
        self,
        client: Redis = None,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
    ):
        """
        Initializes the Redis client.

        Args:
            host (str): Redis server host. Defaults to "localhost".
            port (int): Redis server port. Defaults to 6379.
            db (int): Redis database index. Defaults to 0.
        """
        if client is not None and isinstance(client, Redis):
            self.client = client
        else:
            self.client = redis.Redis(host=host, port=port, db=db)

    def get(self, key: str):
        """
        Retrieves the value associated with the given key from Redis.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            str: The value associated with the key, or None if the key does not exist.

        Raises:
            RedisError: If there is an error during the Redis operation.
        """
        try:
            return self.client.get(key)
        except redis.RedisError as e:
            raise RedisError(str(e))

    def set(self, key: str, value: str, ex: int):
        """
        Sets the value for the given key in Redis.

        Args:
            key (str): The key to set the value for.
            value (str): The value to be set.
            ex (int): Expiration time in seconds for the key.

        Raises:
            RedisError: If there is an error during the Redis operation.
        """
        try:
            self.client.set(key, value, ex=ex)
        except redis.RedisError as e:
            raise RedisError(str(e))

    def incr(self, key: str):
        """
        Increments the value associated with the given key in Redis.

        Args:
            key (str): The key to increment.

        Returns:
            int: The incremented value.

        Raises:
            RedisError: If there is an error during the Redis operation.
        """
        try:
            return self.client.incr(key)
        except redis.RedisError as e:
            raise RedisError(str(e))

    def expire(self, key: str, ex: int):
        """
        Sets an expiration time for the given key in Redis.

        Args:
            key (str): The key to set the expiration for.
            ex (int): Expiration time in seconds for the key.

        Raises:
            RedisError: If there is an error during the Redis operation.
        """
        try:
            self.client.expire(key, ex)
        except redis.RedisError as e:
            raise RedisError(str(e))
