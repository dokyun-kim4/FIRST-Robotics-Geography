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

with open(R"FIRST_LOGO.txt", "r", encoding="UTF-8") as FIRST_LOGO:
    FIRST_LOGO = FIRST_LOGO.read()


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

    with open(f"./FRC{year}.csv", "r", encoding="UTF-8") as data:
        data = pd.read_csv(data)

    for _, row in data.iterrows():
        try:
            current_team = int(row["teamNumber"])

        except ValueError:  # Deals with one row extending down to next column
            continue

        decode_png_one_team(current_team, year)
    print("All PNGs saved successfully")
