import folium
from geopy.geocoders import Nominatim
import pandas as pd


def geo_data(year: int):

    """
    Take a list of locations and return a
    dataframe containing the name,
    latitude, and longitude.

    This will generally work for any location
    name specified. However, if locations have duplicate
    names, the incorrect latitude and longitude may be returned.

    To avoid this, consider qualifying the location with additional
    information. For example, Springfield, CA instead of just Springfield.

    Args:
        location_list (list): A string list of locations

    Returns:
        team_locations (dataframe): A string dataframe
        containing the name, latitude, and longitude.

    """

    team_locations = pd.DataFrame()
    geolocator = Nominatim(user_agent="FRG")

    df = pd.read_csv(f"FRC{year}.csv")
    location_df = df[["city", "stateProv", "schoolName", "teamNumber"]]
    location_school = []
    location_no_school = []
    for _, entry in location_df.iterrows():
        location_string = (
            str(entry["schoolName"]).replace("High School", "")
            + ", "
            + str(entry["city"])
            + ", "
            + str(entry["stateProv"])
        )
        location_school.append(location_string)
    for _, entry in location_df.iterrows():
        location_string = str(entry["city"]) + ", " + str(entry["stateProv"])
        location_no_school.append(location_string)
    location_list = [location_school, location_no_school]
    for address in location_list[0]:
        try:
            location = geolocator.geocode(address, timeout=10)
            name = address
            latitude = location.latitude
            longitude = location.longitude
            current_location = pd.DataFrame(
                {"location": name, "latitude": latitude, "longitude": longitude},
                index=[location_list.index(address)],
            )
            team_locations = pd.concat([team_locations, current_location])
        except AttributeError:
            address_index = location_list[0].index(address)
            address = location_list[1][address_index]
            location = geolocator.geocode(address, timeout=10)
            name = address
            latitude = location.latitude
            longitude = location.longitude
            current_location = pd.DataFrame(
                {"location": name, "latitude": latitude, "longitude": longitude},
                index=[location_list.index(address)],
            )
            team_locations = pd.concat([team_locations, current_location])
            continue

    return team_locations


print(geo_data(2018))
