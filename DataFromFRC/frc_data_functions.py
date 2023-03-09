"""
Imports a list of all FRC teams from 2023 season
Will be pushed by Dokyun
"""
import json
from apitoken import TOKEN
import requests as rq
import pandas as pd


HEADER = {
    "Is-Modified-Since": "",
}


def build_url(year, page):
    """
    Returns a url that directs to a dataset of a given year

    Args:
        year: An integer representing the year

    Returns:
        A URL of the dataset of given year
    """
    return f"https://frc-api.firstinspires.org/v3.0/{str(year)}/teams?page={page}"


def read_text(url):
    """
    Reads text from given url

    Args:
        url: Link to data

    Returns:
        response_text: A string of text from url
    """
    response = rq.get(
        url,
        auth=TOKEN,
        headers=HEADER,
        timeout=10,
    )
    # print(f"Status: {response.status_code}")
    return response.text


def find_cutoff(text):
    """
    Finds the index to split the text into one dictionary and one list of
    dictionaries

    Args:
        text: the data from FIRST API

    Returns:
        cutoff: An integer representing the cutoff index
    """
    for i, char in enumerate(text):

        if char == "[":
            cutoff = i
            return cutoff


def find_page_number(text, cutoff):
    """
    Find how many pages are in a requested FIRST API page

    Args:
        text: The data from FIRST API
        cutoff: An integer representing the cutoff index

    Returns:
        page_num: An integer representing how many pages the requested page has
    """
    total_info_text = text[0:cutoff] + "0}"
    total_dict = json.loads(total_info_text)
    return total_dict["pageTotal"]


def trim_data(text):
    """
    Trims unnecessary information from given data

    Args:
        text: data to trim

    Returns:
        trimmed_text: list of data after trimming
    """
    cutoff = find_cutoff(text)

    trimmed_data = text[cutoff : len(text) - 1]

    return json.loads(trimmed_data)


def extract_data_one_page(year, page):
    """
    Saves data from a specific page from FIRST API of given year to a list

    Args:
       year: An integer representing the year
       page: An integer representing page number

    Returns:
        data_list: A list of all team's information from one page
    """
    url = build_url(year, page)
    text = read_text(url)
    data_list = trim_data(text)

    return data_list


def filter_data(dataframe):
    """
    Removes teams that are outside of the US and Demo teams

    Args:
        dataframe: A pandas dataframe containing all teams from a given year

    Returns:
        final_data: A pandas dataframe that only has non-demo US teams
    """
    only_usa = dataframe[dataframe.country == "USA"]
    final_data = only_usa[only_usa.nameFull != "FIRST Off-Season Demo Team"]
    return final_data


def isolate_team_and_location(dataframe):
    """
    docstring
    """
    dataframe = dataframe[
        ["teamNumber", "nameShort", "city", "stateProv", "schoolName"]
    ]
    return dataframe


def extract_data_all_pages(year):
    """
    Pulls data from all pages from FIRST API of given year and saves as csv

    Args:
        year: An integer representing the year

    Returns:
        filtered_df: A dataframe after filtering
    """

    print(f"Compiling Data for {year}")

    text_for_cutoff = read_text(build_url(year, 1))
    cutoff = find_cutoff(text_for_cutoff)
    pages = find_page_number(text_for_cutoff, cutoff)

    team_info = []
    team_info += extract_data_one_page(year, 1)

    for i in range(2, pages + 1):

        team_info += extract_data_one_page(year, i)

    df = pd.DataFrame(team_info)
    filtered_df = filter_data(df)
    # filtered_df.to_csv(f"FRC{year}.csv")
    return filtered_df


def extract_data_all_years(start, end):
    """
    Creates csv files of a list of teams given a range of years

    Args:
        start: Year to start from
        end: Year to stop at
    """
    for year in range(start, end + 1):
        extract_data_all_pages(year)

    print("ALL DONE!")
