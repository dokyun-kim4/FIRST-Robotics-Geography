"""
Unit tests to verify helper functions used to help scraping
"""


import pytest
from frc_data_functions import find_cutoff

cutoff_cases = [
    # Block of text with no "["
    ("{Apple : 1,Pear : 2}", None),
    # Block of text with "[" at the start
    ("[This is a list]", 0),
    # Block of text with "[" somewhere in the middle
    ("Teams: [{Team :2637,Name :Phantom Catz}]", 7),
    # Block of text with multiple "["s. Should return index of first one
    (
        "Teams: [{Team :2637,Name :Phantom Catz},{Team: 1111, Name: [Comets]}]",
        7,
    ),
]


@pytest.mark.parametrize("text,cutoff", cutoff_cases)
def test_find_cutoff(text, cutoff):
    """
    Tests if find_cutoff() functions as intended

    Args:
        text(str): Text that we want to find the cutoff point of
        cutoff(int): Expected cutoff output from function
    """
    assert (find_cutoff(text)) == cutoff
