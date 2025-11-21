# Data Loading and Environment Variable Setup
import os
import json
import pprint
import urllib.request
import requests
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")
if MAPBOX_TOKEN is None:
    raise RuntimeError("MAPBOX_TOKEN is not set. Check your .env file.")
if MBTA_API_KEY is None:
    raise RuntimeError("MBTA_API_KEY is not set. Check your .env file.")
# Useful base URLs
MAPBOX_URL = "https://api.mapbox.com/search/searchbox/v1/forward"
MBTA_BASE_URL = "https://api-v3.mbta.com/"
MBTA_STOPS_URL = MBTA_BASE_URL + "stops"


def Lati_Long(input_str: str) -> tuple[float, float]:
    """
    Given a place name/address, use Mapbox to return (latitude, longitude).
    """
    params = {
        "q": input_str,
        "access_token": MAPBOX_TOKEN
    }
    response = requests.get(MAPBOX_URL, params=params)
    response.raise_for_status()
    location_data = response.json()

    features = location_data.get("features", [])
    if not features:
        # No result from Mapbox for this query
        raise ValueError(f"No coordinates found for location '{input_str}'")

    # Mapbox coordinates are [longitude, latitude]
    coords = features[0]["geometry"]["coordinates"]
    longitude = coords[0]
    latitude = coords[1]

    # ✅ Return ONLY (lat, lon), not the response object
    return latitude, longitude

def find_stop_near(latitude: float, longitude: float):
    """
    Given latitude and longitude, query the MBTA API for the nearest stop.
    Returns a dict with station_name and wheelchair_accessible, or None if no stop found.
    """
    params = {
        "api_key": MBTA_API_KEY,
        "filter[latitude]": latitude,
        "filter[longitude]": longitude,
        "sort": "distance"
    }

    response = requests.get(MBTA_STOPS_URL, params=params)
    response.raise_for_status()
    station_data = response.json()
    print("MBTA API response:")
    pprint.pprint(station_data)

    data = station_data.get("data", [])

    # ✅ Handle the case where MBTA returns no nearby stops
    if not data:
        return None

    first = data[0]
    station_name = first["attributes"]["name"]
    wheelchair_accessible = first["attributes"]["wheelchair_boarding"] == 1

    return {
        "station_name": station_name,
        "wheelchair_accessible": wheelchair_accessible,
    }

def get_stop_near_place(place: str):
    """
    Convenience function: take a place string,
    convert to coordinates, then call find_stop_near.
    """
    latitude, longitude = Lati_Long(place)
    stop = find_stop_near(latitude, longitude)
    return stop

if __name__ == "__main__":
    print("\n *** Get Current Location ***\n")

    location = input("\n Enter your current location: ")
    try:
        latitude, longitude = Lati_Long(location)
    except ValueError as e:
        print(e)
        exit(1)

    print(f"\n Latitude: {latitude}, Longitude: {longitude} \n")

    stop_info = find_stop_near(latitude, longitude)

    if stop_info is None:
        print("No nearby MBTA station found.")
    else:
        station_name = stop_info["station_name"]
        wheelchair_accessible = stop_info["wheelchair_accessible"]

        print("\n")
        print(f"Nearest MBTA Station: {station_name}")
        print(f"Wheelchair accessible: {wheelchair_accessible}")
