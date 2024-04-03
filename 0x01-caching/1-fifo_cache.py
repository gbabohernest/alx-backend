#!/usr/bin/env python3
"""FIFOCache module that inherits from BaseCaching
"""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache inherits from BaseCaching

     - Implements the put and get methods
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        # keep track of insertion order
        self._keys_in_order = []

    def put(self, key, item):
        """ Add an item to the cache
        """

        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS and \
                    key not in self.cache_data:
                oldest_key = self._keys_in_order.pop(0)
                del self.cache_data[oldest_key]
                print(f"DISCARD: {oldest_key}")

            self.cache_data[key] = item
            self._keys_in_order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is not None or key in self.cache_data:
            return self.cache_data.get(key)
        else:
            return None
