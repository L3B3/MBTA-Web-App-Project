# app.py
"""This file contains the Flask web application routes for the MBTA + Restaurant Finder app.This app allows users to input a location, find the nearest MBTA stop, and see nearby restaurants. It uses the core logic defined in mbta.py to perform these tasks."""
# ========= FLASK APP / ROUTES =========

from flask import Flask, render_template, request
from mbta import get_stop_near_place, get_nearby_restaurants

app = Flask(__name__)


# ----- Main Index Route -----
@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        place = request.form.get("place", "").strip()

        if not place:
            return render_template("index.html", error="Please enter a location.")

        try:
            stop_info, lat, lon = get_stop_near_place(place)
        except ValueError as e:
            # Mapbox couldn't find coordinates
            return render_template("result.html", error=str(e))

        if stop_info is None:
            # MBTA returned no nearby stop
            return render_template(
                "result.html",
                error=f"No MBTA station found near '{place}'. Try another location.",
            )

        restaurants = get_nearby_restaurants(lat, lon)

        return render_template(
            "result.html",
            stop=stop_info,
            place=place,
            restaurants=restaurants,
        )

    # GET request
    return render_template("index.html")
# ----- Run the App -----
if __name__ == "__main__":
    app.run(debug=True)
