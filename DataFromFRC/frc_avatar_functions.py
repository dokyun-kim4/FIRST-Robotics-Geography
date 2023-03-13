"""
Functions to obtain FRC team avatar & save it as .png files
"""
import json
import requests as rq
import pandas as pd
import frc_data_functions as fdf
from apitoken import TOKEN

HEADER = {
    "Is-Modified-Since": "",
}


def build_url(year, team):
    """
    docstring
    """
    return f"https://frc-api.firstinspires.org/v3.0/{year}/avatars?teamNumber={team}"


def get_avatar_one_team(year, team):
    """
    docstring
    """
    response = rq.get(
        url=build_url(year, team),
        auth=TOKEN,
        headers=HEADER,
        timeout=10,
    )
    data = json.loads(response.text)
    return data["teams"]["encodedAvatar"]


print(get_avatar_one_team(2023, 2637))
