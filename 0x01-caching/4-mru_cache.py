#!/usr/bin/env python3
"""MRUCache module that inherits from BaseCaching
"""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRUCache inherits from BaseCaching

        - Implements the put and get methods
    """

    def __init__(self):
        """ Initializes
        """
        super().__init__()
        # Keep track of most recently used keys
        self._most_recently_used = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self._most_recently_used.remove(key)

            elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # cache is full
                mru_key = self._most_recently_used.pop(
                    len(self._most_recently_used) - 1
                )
                del self.cache_data[mru_key]
                print(f"DISCARD: {mru_key}")

            self.cache_data[key] = item
            self._most_recently_used.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is not None or key in self.cache_data:
            if key in self._most_recently_used:
                self._most_recently_used.append(
                    self._most_recently_used.pop(
                        self._most_recently_used.index(key))
                )
            return self.cache_data.get(key)
        else:
            return None
