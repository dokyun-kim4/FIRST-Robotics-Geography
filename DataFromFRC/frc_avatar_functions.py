"""
Functions to obtain FRC team avatar & save it as .png files
"""
import base64
import json
import requests as rq
import pandas as pd
from apitoken import TOKEN

HEADER = {
    "Is-Modified-Since": "",
}


def build_url(year: int, team: int):
    """
    Creates a url that directs to the avatar of a team from a given year

    Args:
        year: An integer representing the year
        team: An integer representing team number

    Returns:
        A url that directs to the avatar of a team from a given year
    """
    return f"https://frc-api.firstinspires.org/v3.0/{year}/avatars?teamNumber={team}"


def get_avatar_one_team(year: int, team: int):
    #Will have to accomodate for teams w/ no avatar (returns 'null')
    """
    Gets the encoded png avatar of a given team in a given year

    Args:
        year: integer representing from what year the avatar should come from
        team: integer representing team number

    Returns:
        A string representing the encoded png avatar
    """
    response = rq.get(
        url=build_url(year, team),
        auth=TOKEN,
        headers=HEADER,
        timeout=10,
    )
    data = json.loads(response.text)
    return data["teams"][0]["encodedAvatar"]


def decode_png(team: int, code: str, year: int):
    """
    Decodes base64 png code and saves a png file

    Args:
      team: An integer representing team name
      code: A string representing the encoded png
    """
    
    with open(f"{year}/{team}.png", "wb") as pic:
        code = bytes(code, "utf-8")
        pic.write(base64.decodebytes(code))


def decode_png_one_year(year: int, dataframe: pd.DataFrame):
    """
    Saves ALL team avatars from one year

    Args:
        dataframe: A pandas dataframe that has team numbers
    """
    data = pd.read_csv(dataframe)
    for _, row in data.iterrows():
        current_team = int(row["teamNumber"])
        current_team_code = get_avatar_one_team(year, current_team)
        decode_png(current_team, current_team_code, year)
