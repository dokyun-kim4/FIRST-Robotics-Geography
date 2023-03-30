"""
Unit tests to verify helper functions used to help scraping
"""

import pytest
import frc_avatar_functions as faf
import frc_data_functions as fdf

data_url_cases = [
    # Given year and single digit page number
    ([2020, 7], "https://frc-api.firstinspires.org/v3.0/2020/teams?page=7"),
    # Given year and double digit page number
    ([2018, 88], "https://frc-api.firstinspires.org/v3.0/2018/teams?page=88"),
]

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

# Import files to test from test_helper_text.txt
with open(R"test_helper_text.txt", "r", encoding="UTF-8") as tests:
    tests = tests.read().splitlines()

page_number_cases = [
    # Given various strings that follows format of posible API outputs
    (tests[0], 71),
    (tests[1], 91),
    (tests[2], 9),
]

trim_data_cases = [
    # Given various strings that follows format of possible API outputs
    (
        tests[0],
        [
            {"Team": 2637, "Name": "Phantom Catz"},
            {"Team": 4414, "Name": "HighTide"},
        ],
    ),
    (tests[1], [{"Team": 2637, "Name": "Phantom Catz"}]),
    (
        tests[2],
        [
            {"Team": 2637, "Name": "Phantom Catz"},
            {"Team": 987, "Name": "HighRollers"},
        ],
    ),
]


avatar_url_cases = [
    # Given year and single digit team number
    (
        [2020, 1],
        "https://frc-api.firstinspires.org/v3.0/2020/avatars?teamNumber=1",
    ),
    # Given year and two digit team number
    (
        [2018, 16],
        "https://frc-api.firstinspires.org/v3.0/2018/avatars?teamNumber=16",
    ),
    # Given year and three digit team number
    (
        [2021, 987],
        "https://frc-api.firstinspires.org/v3.0/2021/avatars?teamNumber=987",
    ),
    # Given year and four digit team number
    (
        [2022, 2637],
        "https://frc-api.firstinspires.org/v3.0/2022/avatars?teamNumber=2637",
    ),
]


@pytest.mark.parametrize("year_and_page,url", data_url_cases)
def test_build_data_url(year_and_page, url):
    """
    Tests if build_url() from frc_data_functions works as intended

    Args:
        year_and_page(list): Contains year(int) and page(int) to request
        data from
        url(str): URL that should direct to correct API page with team info
    """

    assert (fdf.build_url(year_and_page[0], year_and_page[1])) == url


@pytest.mark.parametrize("text,cutoff", cutoff_cases)
def test_find_cutoff(text, cutoff):
    """
    Tests if find_cutoff() functions as intended

    Args:
        text(str): Text that we want to find the cutoff point of
        cutoff(int): Expected cutoff output from function
    """
    assert (fdf.find_cutoff(text)) == cutoff


@pytest.mark.parametrize("text,page", page_number_cases)
def test_find_page_number(text, page):
    """
    Tests if find_page_number() functions as intended

    Args:
        text(str): Text that we want to convert to a dictionary and get the
        value of 'pageTotal'
        page(int): How many pages are in the API output
    """

    assert (fdf.find_page_number(text)) == page


@pytest.mark.parametrize("text,_list", trim_data_cases)
def test_trim_data(text, _list):
    """
    Tests if trim_data() functions as intended

    Args:
        text(str): Text that we want to isolate the list of teams from
        _list(list): Contains dictionaries that contain team info
    """

    assert (fdf.trim_data(text)) == _list


@pytest.mark.parametrize("year_and_team,url", avatar_url_cases)
def test_build_avatar_url(year_and_team, url):
    """
    Tests if build_url() from frc_data_functions works as intended

    Args:
        year_and_team(list): Contains year(int) and team(int) to request
        data from
        url(str): URL that should direct to correct API page with avatar pngs
    """

    assert (faf.build_url(year_and_team[0], year_and_team[1])) == url
