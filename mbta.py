#Data Loading and Environment Variable Setup
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
# Useful base URLs (you need to add the appropriate parameters for each API request)

def Lati_Long(input_str: str) -> tuple[float, float]:
    MAPBOX_URL = "https://api.mapbox.com/search/searchbox/v1/forward"
    params = {
        "q": input_str,
        "access_token": MAPBOX_TOKEN
    }
    response = requests.get(MAPBOX_URL, params=params)
    Location_data = response.json()
    # Always valid for Mapbox
    coords = Location_data["features"][0]["geometry"]["coordinates"]
    #coords = Location_data["features"][0]["geometry"].key_map()
    longitude = coords[0]
    latitude = coords[1]
    return (latitude, longitude)


def find_stop_near(latitude: float, longitude: float) -> tuple[str, bool]:
    MBTA_URL = "https://api-v3.mbta.com/stops"
    params = {
        "filter[latitude]": latitude,
        "filter[longitude]": longitude,
        "sort": "distance",
        "api_key": MBTA_API_KEY
    }
    response = requests.get(MBTA_URL, params=params)
    Station_data = response.json()
    station_name = Station_data["data"][0]["attributes"]["name"]
    wheelchair_accessible = Station_data["data"][0]["attributes"]["wheelchair_boarding"] == 1
    return (station_name, wheelchair_accessible)

def get_stop_near_place(place_name: str) -> tuple[str, bool]:
    latitude, longitude = Lati_Long(place_name)
    return find_stop_near(latitude, longitude)

get_stop_near_place("Boston Common")

if __name__ == "__main__":
    print("\n *** Get Current Location ***\n")

    Location = input("\n Enter your current location: ")
    Latitude, Longitude = Lati_Long(Location)
    
    print(f"\n Latitude: {Latitude}, Longitude: {Longitude} \n")
    station_name, wheelchair_accessible = find_stop_near(Latitude, Longitude)
    get_stop_near_place(Location)
    print("\n")
    print(f"Nearest MBTA Station: {station_name}")