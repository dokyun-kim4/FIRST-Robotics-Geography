def usa_map(team_locations: list, year: int):
    """
    Generate a map of the team locations.

    Args:
        team_locations (dataframe): A string dataframe of locations.

    Returns:
        map_usa (folium.Map): A folium map of US based teams.

    """
    import folium

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

    for index, row in team_locations.iterrows():
        icon = folium.features.CustomIcon(f"{row}.png", icon_size=[20, 20])
        folium.Marker(
            [row["latitude"], row["longitude"]], popup=row["location"], icon=icon
        ).add_to(map_usa)
    return map_usa
