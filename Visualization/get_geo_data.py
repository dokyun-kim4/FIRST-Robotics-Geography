import folium


def geo_data(location_list):

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

    from geopy.geocoders import Nominatim
    import pandas as pd

    team_locations = pd.DataFrame()
    geolocator = Nominatim(user_agent="FRG")

    for address in location_list:
        location = geolocator.geocode(address)
        name = address
        lattitude = location.latitude
        longitude = location.longitude
        current_location = pd.DataFrame(
            {"location": name, "latitude": lattitude, "longitude": longitude},
            index=[location_list.index(address)],
        )
        team_locations = pd.concat([team_locations, current_location])
    return team_locations
