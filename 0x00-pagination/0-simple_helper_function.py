#!/usr/bin/env python3
"""
Write a function named index_range that takes two integer
arguments page and page_size.

The function should return a tuple of size two containing
a start index and an end index corresponding to the range
of indexes to return in a list for those particular pagination
parameters.

Page numbers are 1-indexed, i.e. the first page is page 1.
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
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
