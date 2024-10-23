#!/usr/bin/env python3
"""
Create a Cache class for interacting with Redis.
"""
import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def call_history(method: Callable) -> Callable:
    """stores the history of inputs and outputs for a
    particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """ adds input and output history to Redis
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_list_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, output)
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """ count the number of times a method is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """cACHE CLASS"""
    def __init__(self):
        """initializes a Redis client instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

        @call_history
        @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method: tore data in Redis and return a key for the stored"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn:
            Optional[Callable[[bytes], Union[str, bytes, int,     float]]] =
            None) -> Union[str, bytes, int, float, None]:
        """get data from Redis & optionally apply a conversio
            """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """get string"""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """retrieve data as integer"""
        return self.get(key, lambda i: int(i))
