"""
Functions for generating the US map with markers
"""

import os
import pandas as pd
import folium
import folium.plugins as fp
from natural_sort import natural_sort


def usa_map_initialize() -> folium.Map:
    """
    Defines the us_map template for visualizing different types of data

    Returns:
        map_usa: folium map object with blank map of the US
    """
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

    return map_usa


def usa_map_with_avatar(year: int) -> folium.Map:
    """
    Generate a map of the team locations.

    Args:
        year (int): Indicates which year's avatar to use

    Returns:
        map_usa (folium.Map): A folium map of US based teams.

    """
    team_locations = pd.read_csv(f"../Location/{year}/{year}Location.csv")
    map_usa = usa_map_initialize()

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


def markercluster_map(year: int) -> folium.Map:
    """
    Generate a map of the team locations with markercluster implemented.

    Args:
        year (int): Indicates which year's avatar to use

    Returns:
        map_usa (folium.Map): A folium map of US based teams.

    """
    avatar_url = f"../Avatars/{year}"
    pictures = natural_sort(os.listdir(avatar_url))

    team_locations = pd.read_csv(f"../Location/{year}/{year}Location.csv")
    map_usa = usa_map_initialize()

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

    fp.MarkerCluster(
        locations=coordinates, popups=maptexts, icons=avatars
    ).add_to(map_usa)

    return map_usa


def heat_map(year):
    """
    Generate a heatmap for a given year.

    Args:
        year: An integer specifying the year to visualize.

    Returns:
        heatmap_map (folium.Map): A folium heatmap of US based teams.

    """
    team_locations = pd.read_csv(f"../Location/{year}/{year}Location.csv")
    heatmap_map = usa_map_initialize()

    team_lat_long = team_locations[["latitude", "longitude"]]
    fp.HeatMap(
        team_lat_long, gradient={0.4: "blue", 0.65: "white", 0.8: "red"}
    ).add_to(heatmap_map)
    return heatmap_map


def add_sponsor(us_map: folium.Map) -> folium.Map:
    """
    Plots FRC sponsors on a pre-existing US map

    Args:
        us_map: A folium map object to plot sponsor markers on

    Returns:
        us_map: Map object that has sponsor locations on it
    """
    sponsor_locations = pd.read_csv("../Location/Sponsors.csv")

    for _, row in sponsor_locations.iterrows():
        marker_text = row["name"]
        folium.Marker(
            [row["latitude"], row["longitude"]],
            popup=marker_text,
        ).add_to(us_map)

    return us_map
