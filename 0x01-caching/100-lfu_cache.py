#!/usr/bin/env python3
"""LFUCache module that inherits from BaseCaching
"""


from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFUCache inherits from BaseCaching

      - Implements the put and get methods
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        # Keep track of keys & min_key frequency
        self.keys_frequency = {}
        self.keys_min_frequency = 0

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        # If key exists, update value and increase key frequency
        if key in self.cache_data:
            self.cache_data[key] = item
            self.keys_frequency[key] += 1
            self.keys_min_frequency = min(self.keys_frequency.values())
            return

        # If cache_data is full, remove the least frequently used item
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            min_freq_keys = [k for k, v in self.keys_frequency.items()
                             if v == self.keys_min_frequency]
            lfu_key = min_freq_keys[0]  # In case of tie, remove the first one
            del self.cache_data[lfu_key]
            del self.keys_frequency[lfu_key]
            print(f"DISCARD: {lfu_key}")

        # Add new key-value pair
        self.cache_data[key] = item
        self.keys_frequency[key] = 1
        self.keys_min_frequency = 1 if len(self.cache_data) == 1\
            else min(self.keys_frequency.values())

    def get(self, key):
        """ Get an item by key
        """
        if key not in self.cache_data:
            return None

        # Increase the frequency of the accessed item
        self.keys_frequency[key] += 1

        # Update min_frequency if needed
        self.keys_min_frequency = min(self.keys_frequency.values())

        return self.cache_data[key]
