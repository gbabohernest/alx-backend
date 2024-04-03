#!/usr/bin/env python3
"""LRUCache module that inherits from BaseCaching
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRUCache inherits from BaseCaching

     - Implements the put and get methods
     """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        # Keep track of least recently used keys
        self._least_recently_used = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self._least_recently_used.remove(key)
            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lru_key = self._least_recently_used.pop(0)
                del self.cache_data[lru_key]
                print(f"DISCARD: {lru_key}")

            self.cache_data[key] = item
            self._least_recently_used.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is not None or key in self.cache_data:
            if key in self._least_recently_used:
                self._least_recently_used.append(
                    self._least_recently_used.pop(
                        self._least_recently_used.index(key))
                )
            return self.cache_data.get(key)

        else:
            return None
