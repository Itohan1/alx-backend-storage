#!/usr/bin/env python3
"""
   Create a Cache class. In
   the __init__ method, store an
   instance of the Redis client
   as a private variable named _redis
   (using redis.Redis()) and flush
   the instance using flushdb.

   Create a store method that
   takes a data argument and returns
   a string. The method should generate
   a random key (e.g. using uuid),
   store the input data in Redis using
   the random key and return the key.

   Type-annotate store correctly.
   Remember that data can be a
   str, bytes, int or float
"""
from typing import Union, Callable, Optional
import redis
import uuid
import functools


def count_calls(method: Callable) -> Callable:
    """Count calls"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """modifies the functionality of a class method"""
        key = method.__qualname__
        count = self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """python interraction with reddit"""

    def __init__(self):
        """store instance of Redit into _redit"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """returns the unique identify for storaging data"""

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Optional[Union[str, bytes, int, float]]:
        """Retrive the desired format with callable function"""

        data = self._redis.get(key)

        if not data:
            return None

        if fn:
            return fn(data)

        return data

    def get_str(self, key: str) -> Optional[str]:
        """The return value of the desired format is a string"""

        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """The return value of the desired format is an integer"""

        return self.get(key, fn=int)
