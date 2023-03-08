"""
Imports a list of all FRC teams from 2023 season
Will be pushed by Dokyun
"""

import requests as rq
import pandas as pd
import json

TOKEN = ("dkim4", "dd3338ba-b90d-473d-96bc-ead9bd88e480")
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
    DOCSTRING HERE
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
        trimmed_text: data after trimming
    """
    for i, char in enumerate(text):
        if char == "[":
            cutoff = i

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


def extract_data_all_pages(year):
    """
    Pulls data from all pages from FIRST API of given year and saves as csv

    Args:
        year: An integer representing the year

    """
    print("Compiling Data...")
    text_for_cutoff = read_text(build_url(year, 1))
    pages = find_page_number(text_for_cutoff, find_cutoff(text_for_cutoff))
    print(pages)
    team_info = []
    team_info += extract_data_one_page(year, 1)

    for i in range(2, int(pages / 2)):

        team_info += extract_data_one_page(year, i)

    df = pd.DataFrame(team_info)
    df.to_csv(f"FRC{year}.csv")


def extract_data_all_years():
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    for year in years:
        extract_data_all_pages(year)
