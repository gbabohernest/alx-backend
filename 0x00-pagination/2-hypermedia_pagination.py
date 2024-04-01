#!/usr/bin/env python3
"""
Defines a Server class to paginate a database of popular baby names.
"""

import csv
import math
from typing import List, Tuple, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Instantiate the server"""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Get a page of data from the dataset based on pagination parameters.
        :param page: (int) Page number, default is 1
        :param page_size: (int) Page size, default is 10
        :return: List of rows corresponding to the requested page.
        """

        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0

        start_index, end_index = self.index_range(page, page_size)

        data_set = self.dataset()

        # check if the indexes are out of range
        if start_index >= len(data_set):
            return []

        # get page data by slicing
        page_data = data_set[start_index:end_index]

        return page_data

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Get hyperdata including page size, current page number,
        dataset page, next page number, previous page number, and
        total number of pages.

        :param page: (int) Page number, default is 1
        :param page_size: (int) Page size, default is 10
        :return: Dictionary containing hyperdata.
        """

        # assert isinstance(page, int) and isinstance(page_size, int)
        # assert page > 0 and page_size > 0

        data = self.get_page(page, page_size)
        # print(len(self.dataset()))

        total_pages = math.ceil(len(self.dataset()) / page_size)

        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        hyperdata = {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }

        return hyperdata

    def index_range(self, page: int, page_size: int) -> Tuple[int, int]:
        """
        A simple helper function
        :param page: (int) page number
        :param page_size: (int) page size
        :return: A tuple of size two containing start index
                 and end index
        """

        page -= 1

        start_index = page * page_size
        end_index = (page + 1) * page_size

        return start_index, end_index
