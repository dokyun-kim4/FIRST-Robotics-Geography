"""
Functions to obtain FRC team avatar & save it as .png files
"""
import base64
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
    return data["teams"][0]["encodedAvatar"]


def decode_png(team, code):
    """
    Decodes base64 png code and saves a png file

    Args:
      team: An integer representing team name
      code: A string representing the encoded png
    """

    with open(f"{team}.png", "wb") as pic:
        code = bytes(code, "utf-8")
        pic.write(base64.decodebytes(code))


print(get_avatar_one_team(2018, 4087))
decode_png(4087, get_avatar_one_team(2018, 4087))
