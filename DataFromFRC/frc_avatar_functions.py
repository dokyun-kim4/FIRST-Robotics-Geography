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

FIRST_LOGO = "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"


def build_url(year: int, team: int) -> str:
    """
    Creates a url that directs to the avatar of a team from a given year

    Args:
        year: An integer representing the year
        team: An integer representing team number

    Returns:
        A url that directs to the avatar of a team from a given year
    """
    return f"https://frc-api.firstinspires.org/v3.0/{year}/avatars?teamNumber={team}"


def decode_png_one_team(team: int, year: int):
    """
    Decodes base64 png code and saves a png file

    Args:
      team: An integer representing team name
      code: A string representing the encoded png
    """

    def get_avatar_one_team(year: int, team: int) -> str:
        # Will have to accomodate for teams w/ no avatar (returns 'null')
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
            timeout=100,
        )
        data = json.loads(response.text)
        try:
            return data["teams"][0]["encodedAvatar"]
        except IndexError:
            return FIRST_LOGO

    code = get_avatar_one_team(year, team)
    with open(f"Avatars/{year}/{team}.png", "wb+") as pic:
        code = bytes(code, "utf-8")
        pic.write(base64.decodebytes(code))


def decode_png_one_year(year: int):
    """
    Saves ALL team avatars from one year

    Args:
        year: integer reprenting which year to pull from
    """
    print(f"Saving PNGs from year {year}")
    data = pd.read_csv(
        open(f"./FRC{year}.csv", "r", encoding="UTF-8"), engine="c"
    )

    for _, row in data.iterrows():
        try:
            current_team = int(row["teamNumber"])

        except ValueError:  # Deals with one row extending down to next column
            continue

        decode_png_one_team(current_team, year)
    print("All PNGs saved successfully")
