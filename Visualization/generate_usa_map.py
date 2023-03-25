"""
Functions for generating the US map with markers
"""
import pandas as pd
import folium
import folium.plugins as fp
import re
import os


def alphanumeric_sort(data: list) -> list:
    """
    Sorts files in a given list alphanumerically

    Args:
        data: A list of entries that are out of order

    Returns:
        A sorted list of entries
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(data, key=alphanum_key)


def usa_map(year: int):
    """
    Generate a map of the team locations.

    Args:
        team_locations (dataframe): A string dataframe of locations.

    Returns:
        map_usa (folium.Map): A folium map of US based teams.

    """
    team_locations = pd.read_csv(f"../Location/{year}/{year}Location.csv")
    max_bounds = [[3, -180], [73, -50]]
    map_usa = folium.Map(
        location=[37.0902, -95.7129],
        width="%100",
        height="%100",
        zoom_start=5,
        min_zoom=5,
        max_zoom=18,
        max_bounds=max_bounds,
        min_lat=12,
        max_lat=70,
        min_lon=-180,
        max_lon=-30,
        prefer_canvas=True,
    )

    for _, row in team_locations.iterrows():

        if year >= 2018:
            icon = folium.features.CustomIcon(
                f"../Avatars/{year}/{row['teamNumber']}.png", icon_size=[20, 20]
            )
        else:
            icon = folium.features.CustomIcon(
                "../Avatars/default.png", icon_size=[20, 20]
            )

        marker_text = f"#{row['teamNumber']} \n {row['nameShort']}"
        folium.Marker(
            [row["latitude"], row["longitude"]], popup=marker_text, icon=icon
        ).add_to(map_usa)
    return map_usa


def markercluster_map(year: int):
    """
    Generate a map of the team locations with markercluster implemented.

    Args:
        team_locations (dataframe): A string dataframe of locations.

    Returns:
        map_usa (folium.Map): A folium map of US based teams.

    """
    avatar_url = f"../Avatars/{year}"
    pictures = alphanumeric_sort(os.listdir(avatar_url))

    team_locations = pd.read_csv(f"../Location/{year}/{year}Location.csv")
    max_bounds = [[3, -180], [73, -50]]
    map_usa = folium.Map(
        location=[37.0902, -95.7129],
        width="%100",
        height="%100",
        zoom_start=5,
        min_zoom=5,
        max_zoom=18,
        max_bounds=max_bounds,
        min_lat=12,
        max_lat=70,
        min_lon=-180,
        max_lon=-30,
        prefer_canvas=True,
    )

    coordinates = []
    maptexts = []
    avatars = []

    for _, row in team_locations.iterrows():

        coordinate = [row["latitude"], row["longitude"]]
        coordinates.append(coordinate)

        name = f"#{row['teamNumber']} \n {row['nameShort']}"
        maptexts.append(name)

    for png in pictures:
        full_path = avatar_url + "/" + png
        icon = folium.features.CustomIcon(full_path, icon_size=[20, 20])
        avatars.append(icon)

    print(len(coordinates))
    print(len(maptexts))
    print(len(avatars))
    fp.MarkerCluster(locations=coordinates, popups=maptexts, icons=avatars).add_to(
        map_usa
    )

    return map_usa
