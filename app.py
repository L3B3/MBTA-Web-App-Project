from flask import Flask
from mbta import find_stop_near, get_stop_near_place, Lati_Long
app = Flask(__name__)

@app.route("/")
def welcome():
    return 'Hey there, lovely to see you and welcome to the "Best" MBTA Web App!'

@app.route("/where-are-you")
def where_are_you():
    place = request.args.get("place")  # e.g. /where-are-you?place=Boston

    if not place:
        return "Please provide a location with ?place=Your+Location", 400

    latitude, longitude = Lati_Long(place)

    return f"Your location '{place}' has coordinates: ({latitude}, {longitude})"

@app.route("/mbta-stop-near-me")
def mbta_stop_near_me():
    place = request.args.get("place")  # e.g. /mbta-stop-near-me?place=Boston

    if not place:
        return "Please provide a location with ?place=Your+Location", 400

    # Get latitude/longitude from Mapbox
    latitude, longitude = Lati_Long(place)

    # Use those coordinates to find the closest stop
    station_name, wheelchair_accessible = find_stop_near(latitude, longitude)

    return (
        f"The nearest MBTA stop to '{place}' is {station_name}. "
        f"Wheelchair accessible: {wheelchair_accessible}"
    )

if __name__ == "__main__":
    app.run(debug=True)
