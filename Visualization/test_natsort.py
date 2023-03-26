"""
Test functions used to perform natural sort on a given list of
common filename formats
"""

from collections import Counter
import pytest

from natural_sort import (
    make_natural_key,
    natural_sort,
)

natural_key_cases = [
    # File name with only number(s)
    ("1.jpg", ["", 1, ".jpg"]),
    ("11.jpg", ["", 11, ".jpg"]),
    ("111.jpg", ["", 111, ".jpg"]),
    # File name with a non-number character in front of the number(s)
    ("_71.txt", ["_", 71, ".txt"]),
    ("abc67.png", ["abc", 67, ".png"]),
    # File name with two number groups and non-number chacter(s) in between
    ("89_2021.csv", ["", 89, "_", 2021, ".csv"]),
    ("12_team2637.mov", ["", 12, "_team", 2637, ".mov"]),
]

natural_sort_cases = [
    # Files with only numbers
    (["10.jpg", "1.jpg"], ["1.jpg", "10.jpg"]),
    (
        ["56.jpg", "128.jpg", "4.jpg", "999.jpg"],
        ["4.jpg", "56.jpg", "128.jpg", "999.jpg"],
    ),
    # Files with numbers & same characters
    (
        ["abc78.txt", "abc71.txt", "abc7.txt"],
        ["abc7.txt", "abc71.txt", "abc78.txt"],
    ),
]


@pytest.mark.parametrize("text,key", natural_key_cases)
def test_make_natural_key(text, key):
    """
    ds
    """
    assert Counter(make_natural_key(text)) == Counter(key)


@pytest.mark.parametrize("original_list,sorted_list", natural_sort_cases)
def test_natural_sort(original_list, sorted_list):
    """
    ds
    """

    assert Counter(natural_sort(original_list)) == Counter(sorted_list)
