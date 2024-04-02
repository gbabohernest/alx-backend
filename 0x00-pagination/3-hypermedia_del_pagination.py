#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
            return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Get hyperdata by index including current start index,
        next index, page size, and actual data for the page.

        :param index: (int) Current start index, default is None
        :param page_size: (int) Page size, default is 10
        :return: Dictionary containing hyperdata by index
        """

        if index is None:
            index = 0

        assert isinstance(index, int) and isinstance(page_size, int)

        assert 0 <= index < len(self.__indexed_dataset)

        next_index = min(index + page_size, len(self.__indexed_dataset))

        data = []

        current_index = index
        while current_index < next_index:
            if current_index in self.__indexed_dataset:
                data.append(self.__indexed_dataset[current_index])
            else:
                # if current index is missing, move to the next one
                next_index += 1
            current_index += 1

        hyperdata = {
            'index': index,
            'data': data,
            'page_size': page_size,
            'next_index': next_index
        }

        return hyperdata
