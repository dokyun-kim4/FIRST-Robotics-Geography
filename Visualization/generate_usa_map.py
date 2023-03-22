import pandas as pd
import folium
import folium.plugins as fp


def usa_map(year):
    """
    Generate a map of the team locations.

    Args:
        team_locations (dataframe): A string dataframe of locations.

    Returns:
        map_usa (folium.Map): A folium map of US based teams.

    """
    team_locations = pd.read_csv(f"{year}Location.csv")
    max_bounds = [[3, -180], [73, -50]]
    map_usa = folium.Map(
        location=[37.0902, -95.7129],
        width="%100",
        height="%100",
        zoom_start=5,
        min_zoom=5,
        max_zoom=12,
        max_bounds=max_bounds,
        min_lat=12,
        max_lat=70,
        min_lon=-180,
        max_lon=-30,
    )

    for _, row in team_locations.iterrows():
        icon = folium.features.CustomIcon(
            f"../Avatars/{year}/{row['teamNumber']}.png", icon_size=[20, 20]
        )
        marker_text = f"#{row['teamNumber']}"
        folium.Marker(
            [row["latitude"], row["longitude"]], popup=marker_text, icon=icon
        ).add_to(map_usa)
    # for _, row in team_locations.iterrows():
    #     # icon = folium.features.CustomIcon(f"{row}.png", icon_size=[20, 20])
    #     marker_text = f"#{row['teamNumber']}"
    #     fp.MarkerCluster(
    #         [row["latitude"], row["longitude"]],
    #         popup=marker_text,  # icon=icon#
    #     ).add_to(map_usa)
    return map_usa
