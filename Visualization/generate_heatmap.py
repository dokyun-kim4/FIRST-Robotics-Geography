import pandas as pd
import folium
import folium.plugins as fp


def heatmap(year):
    """
    Generate a heatmap for a given year.

    Args:
        year: An integer specifying the year to visualize.

    Returns:
        heatmap_map (folium.Map): A folium heatmmap of US based teams.

    """
    team_locations = pd.read_csv(f"../Location/{year}/{year}Location.csv")
    max_bounds = [[3, -180], [73, -50]]
    heatmap_map = folium.Map(
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
        prefer_canvas=True,
    )
    team_lat_long = team_locations[["latitude", "longitude"]]
    fp.HeatMap(team_lat_long, gradient={0.4: "blue", 0.65: "white", 1: "red"}).add_to(
        heatmap_map
    )
    return heatmap_map
