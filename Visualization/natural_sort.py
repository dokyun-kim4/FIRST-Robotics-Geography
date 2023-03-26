"""
Necessary functions to perform a natural sort (alphanumeric sort)
"""

import re


def make_natural_key(text: str) -> list[str or int]:
    """
    Takes a string and splits it into integer and text component
    Ex: "123.txt" -> ["",123]

    Args:
        text: A string that has numbers and characters

    Returns:
        key: A list with an integer component and a text component
    """
    pattern = re.compile("([0-9]+)")
    key = []
    for part in pattern.split(text):
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part)

    return key


def natural_sort(data: list[str]) -> list[str]:
    """
    Performs a natural sort on a given list
    Ex: ['1.jpg','78.jpg','761.jpg','16.jpg','5.jpg'] will return
        ['1.jpg','5.jpg','16.jpg','78.jpg','761.jpg']

    Args:
        data: A list with strings

    Return:
        sorted_data: A list with strings that are sorted alphanumerically
    """
    sorted_data = sorted(data, key=make_natural_key)
    return sorted_data
