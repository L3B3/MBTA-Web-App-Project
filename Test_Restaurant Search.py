"""
Quick test script for MBTA + restaurant search.

Run with:
    python test_mbta_restaurants.py
"""

from pprint import pprint

from mbta import get_stop_near_place, get_nearby_restaurants

def test_location(place: str, max_to_show: int = 5) -> None:
    print("=" * 60)
    print(f"Testing location: {place}")
    print("=" * 60)

    # 1. Get nearest MBTA stop + coordinates
    try:
        stop_info, lat, lon = get_stop_near_place(place)
    except Exception as e:
        print(f"[ERROR] get_stop_near_place('{place}') raised an exception:")
        print(e)
        return

    if stop_info is None:
        print(f"[FAIL] No MBTA stop found near '{place}'.")
        return

    print("[OK] Nearest MBTA stop found:")
    print(f"  Station Name        : {stop_info['station_name']}")
    print(f"  Wheelchair Accessible: {stop_info['wheelchair_accessible']}")
    print(f"  Coordinates (lat,lon): ({lat}, {lon})")
    print()

    # 2. Get nearby restaurants using SerpAPI
    try:
        restaurants = get_nearby_restaurants(lat, lon)
    except Exception as e:
        print(f"[ERROR] get_nearby_restaurants(...) raised an exception:")
        print(e)
        return

    if not restaurants:
        print("[WARN] No restaurants returned for this location.")
    else:
        print(f"[OK] Found {len(restaurants)} nearby restaurants.")
        print(f"Showing up to {max_to_show} of them:\n")
        for r in restaurants[:max_to_show]:
            name = r.get("name")
            rating = r.get("rating")
            address = r.get("address")
            phone = r.get("phone")
            print(f"  • {name}")
            if address:
                print(f"      Address: {address}")
            if rating is not None:
                print(f"      Rating : {rating}/5")
            if phone:
                print(f"      Phone  : {phone}")
            print()

    print("Test completed for:", place)
    print()


if __name__ == "__main__":
    # Try a few busy locations that should have lots of restaurants
    test_location("Boston Common")
    test_location("Fenway Park, Boston MA")
    test_location("Harvard Square, Cambridge MA")
