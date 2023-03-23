import folium
from geopy.geocoders import Nominatim
import pandas as pd
import time


def geo_data(year: int, start: int, end: int) -> pd.DataFrame:

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
    print(f"Compiling latitude and longitude of teams from {year}")

    team_locations = pd.DataFrame()
    geolocator = Nominatim(user_agent="FRG")

    df = pd.read_csv(f"FRC{year}.csv")
    location_df = df[["city", "stateProv", "schoolName", "teamNumber", "nameShort"]]

    location_list = []

    for _, entry in location_df.iterrows():
        original = (
            str(entry["schoolName"]).replace("High School", "")
            + ", "
            + str(entry["city"])
            + ", "
            + str(entry["stateProv"])
        )

        city_state = str(entry["city"]) + ", " + str(entry["stateProv"])
        state = str(entry["stateProv"])
        location_list.append([original, city_state, state])

    if len(location_list) <= end:
        end = len(location_list)

    for i, address in enumerate(location_list[start:end]):
        print(i)

        location = None
        address_idx = 0
        while location is None and address_idx < 3:

            location = geolocator.geocode(address[address_idx], timeout=9999)
            address_idx += 1

        if location is not None:

            name = address[address_idx - 1]

            latitude = location.latitude
            longitude = location.longitude
            current_location = pd.DataFrame(
                {
                    "teamNumber": location_df.iloc[i + start]["teamNumber"],
                    "nameShort": location_df.iloc[i + start]["nameShort"],
                    "location": name,
                    "latitude": latitude,
                    "longitude": longitude,
                },
                index=[location_list.index(address)],
            )
            team_locations = pd.concat([team_locations, current_location])

    print("Done")
    print("converting csv")
    team_locations.to_csv(f"Location/{year}/{start}-{end}.csv")
    return team_locations


geo_data(2015, 2500, 3000)
