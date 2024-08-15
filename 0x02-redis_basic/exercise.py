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
from typing import Union, Callable, Optional, Any
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


def call_history(method: Callable) -> Callable:
    """Check input and outputs"""

    @functools.wraps(method)
    def wrapper(self, *args) -> Any:
        """Modify the method"""
        outputs = f"{method.__qualname__}:outputs"
        inputs = f"{method.__qualname__}:inputs"

        self._redis.rpush(inputs, str(args))
        result = method(self, *args)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def replay(method: Callable) -> map:
    """display a method used"""

    self = method.__self__
    inputs = self._redis.lrange("{}:inputs".format(method.__qualname__), 0, -1)
    outputs = self._redis.lrange("{}:outputs".format(
        method.__qualname__), 0, -1)
    get_calls = int(self._redis.get(method.__qualname__))
    if get_calls is None:
        get_calls = 0
    print(f"{method.__qualname__} was called {get_calls} times:")
    for i, j in zip(inputs, outputs):
        i = i.decode('utf-8')
        j = j.decode('utf-8')
        print(f"{method.__qualname__}(*{i}) -> {j}")


class Cache:
    """python interraction with reddit"""

    def __init__(self):
        """store instance of Redit into _redit"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
