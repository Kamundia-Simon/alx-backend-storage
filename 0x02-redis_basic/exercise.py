#!/usr/bin/env python3
"""
Create a Cache class for interacting with Redis.
"""
import redis
import uuid
from typing import Union


class Cache:
    """cACHE CLASS"""
    def __init__(self):
        """initializes a Redis client instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method: tore data in Redis and return a key for the stored"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
