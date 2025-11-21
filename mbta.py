# mbta.py
"""This file is set up to contain the core MBTA / Mapbox / SerpAPI logic.
You can run this file directly to do manual testing of the functions and confirm they work."""
# ========= CORE MBTA / MAPBOX / SERPAPI LOGIC =========

import os
import json
import requests
from dotenv import load_dotenv

# ----- Environment & API Setup -----
load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if MAPBOX_TOKEN is None:
    raise RuntimeError("MAPBOX_TOKEN is not set. Check your .env file.")
if MBTA_API_KEY is None:
    raise RuntimeError("MBTA_API_KEY is not set. Check your .env file.")
if SERPAPI_KEY is None:
    raise RuntimeError("SERPAPI_KEY is not set. Check your .env file.")

MAPBOX_URL = "https://api.mapbox.com/search/searchbox/v1/forward"
MBTA_BASE_URL = "https://api-v3.mbta.com/"
MBTA_STOPS_URL = MBTA_BASE_URL + "stops"


# ----- Geocoding (Mapbox) -----
def Lati_Long(input_str: str) -> tuple[float, float]:
    """
    Given a place name or address, return (latitude, longitude)
    using the Mapbox Search API.
    """
    params = {
        "q": input_str,
        "access_token": MAPBOX_TOKEN,
    }
    response = requests.get(MAPBOX_URL, params=params)
    response.raise_for_status()
    location_data = response.json()

    features = location_data.get("features", [])
    if not features:
        raise ValueError(f"No coordinates found for location '{input_str}'")

    # Mapbox coordinates are [longitude, latitude]
    coords = features[0]["geometry"]["coordinates"]
    longitude = coords[0]
    latitude = coords[1]

    return latitude, longitude


# ----- MBTA Stop Lookup -----
def find_stop_near(latitude: float, longitude: float):
    """
    Given latitude and longitude, query the MBTA API for the nearest stop.
    Returns a dict with station_name and wheelchair_accessible,
    or None if no stop is found.
    """
    params = {
        "api_key": MBTA_API_KEY,
        "filter[latitude]": latitude,
        "filter[longitude]": longitude,
        "sort": "distance",
    }

    response = requests.get(MBTA_STOPS_URL, params=params)
    response.raise_for_status()
    station_data = response.json()

    data = station_data.get("data", [])
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
    Convenience function:
    - Convert a place string to coordinates
    - Look up the nearest MBTA stop
    Returns (stop_info, latitude, longitude).
    """
    latitude, longitude = Lati_Long(place)
    stop = find_stop_near(latitude, longitude)
    return stop, latitude, longitude


# ----- Nearby Restaurants (SerpAPI / Google Maps) -----
def get_nearby_restaurants(
    latitude: float,
    longitude: float,
    query: str = "restaurants",
    limit: int = 9,
):
    """
    Use SerpAPI's Google Maps engine to find nearby restaurants.
    Returns a list of up to `limit` restaurant dicts with:
    - name
    - rating
    - address
    - phone
    """
    params = {
        "engine": "google_maps",
        "type": "search",
        "q": query,
        "ll": f"@{latitude},{longitude},14z",
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "google_domain": "google.com",
    }

    response = requests.get("https://serpapi.com/search", params=params)
    response.raise_for_status()
    data = response.json()

    if "error" in data:
        raise RuntimeError(f"SerpAPI error: {data['error']}")

    restaurants = []
    for r in data.get("local_results", []):
        restaurants.append(
            {
                "name": r.get("title"),
                "rating": r.get("rating"),
                "address": r.get("address"),
                "phone": r.get("phone"),
            }
        )

    return restaurants[:limit]
# ----- Main block for manual testing -----
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
