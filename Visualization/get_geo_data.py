"""
Sets of functions necessary to scrape and organize coordinates of FRC teams
"""
import os
from geopy.geocoders import Nominatim
import pandas as pd


def geo_data(year: int, start: int, end: int) -> pd.DataFrame:
    """
    Take a list of locations and return a
    dataframe containing the name,number
    latitude, and longitude.

    This will generally work for any location
    name specified. However, if locations have duplicate
    names, the incorrect latitude and longitude may be returned.

    To avoid this, consider qualifying the location with additional
    information. For example, Springfield, CA instead of just Springfield.

    Due to HTML timeout errors, the scraping is done in pieces.
    Instead of querying all 3000 locations at once, we will query slices of it.
    Ex: 0 to 500, 500 to 1000, 1000 to 1500, etc.

    Args:
        year: Integer representing which year's data to scrape coordinates
        start: Integer representing start index
        end: Integer represengint end index


    Returns:
        team_locations (dataframe): A string dataframe
        containing the Team name,Team number, latitude, and longitude.

    """
    print(f"Compiling latitude and longitude of teams from {year}")

    team_locations = pd.DataFrame()
    geolocator = Nominatim(user_agent="FRG")

    # data_frame = pd.read_csv(
    #     open(f"FRC{year}.csv", "r", encoding="UTF-8"), engine="c"
    # )

    with open(f"FRC{year}.csv", "r", encoding="UTF-8") as data_frame:
        data_frame = pd.read_csv(data_frame)

    location_df = data_frame[
        ["city", "stateProv", "schoolName", "teamNumber", "nameShort"]
    ]

    location_list = []

    for _, entry in location_df.iterrows():
        location_list.append(
            (
                str(entry["schoolName"]).replace("High School", "")
                + ", "
                + str(entry["city"])
                + ", "
                + str(entry["stateProv"])
            ),
            str(entry["city"]) + ", " + str(entry["stateProv"]),
            str(entry["stateProv"]),
        )
        # original = (
        #     str(entry["schoolName"]).replace("High School", "")
        #     + ", "
        #     + str(entry["city"])
        #     + ", "
        #     + str(entry["stateProv"])
        # )

        # city_state = str(entry["city"]) + ", " + str(entry["stateProv"])
        # state = str(entry["stateProv"])
        # location_list.append([original, city_state, state])

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

            current_location = pd.DataFrame(
                {
                    "teamNumber": location_df.iloc[i + start]["teamNumber"],
                    "nameShort": location_df.iloc[i + start]["nameShort"],
                    "location": name,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                },
                index=[location_list.index(address)],
            )
            team_locations = pd.concat([team_locations, current_location])

    print("Done")
    print("converting csv")
    team_locations.to_csv(f"Location/{year}/{start}-{end}.csv")
    return team_locations


def merge_csv(year: int):
    """
    Takes csvs in a folder and combines them into one csv file

    Args:
        year: integer representing which year the data came from
    """
    folder_path = f"./Location/{year}/"
    csvs = os.listdir(folder_path)
    dataframes = []
    print(csvs)
    for filename in csvs:
        csv_path = folder_path + filename
        dataframes.append(pd.read_csv(csv_path, index_col=False))

    merged = pd.concat(dataframes)
    merged = merged.sort_values("teamNumber")

    merged.to_csv(f"Location/{year}/{year}Location.csv", index=False)


