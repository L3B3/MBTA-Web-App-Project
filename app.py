from flask import Flask, render_template, request
from mbta import get_stop_near_place  # you don't actually need find_stop_near or Lati_Long here

app = Flask(__name__)


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        place = request.form.get("place", "").strip()

        if not place:
            # User submitted empty form
            return render_template("index.html",
                                   error="Please enter a location.")

        # Call your helper from mbta.py
        stop_info = get_stop_near_place(place)

        if stop_info is None:
            # No station found – show a friendly message instead of 500
            return render_template(
                "result.html",
                error=f"No MBTA station found near '{place}'. Try another location.",
            )

        # Success: show the result page
        return render_template("result.html", stop=stop_info, place=place)

    # GET request: just render the main form
    return render_template("index.html")


# If you really want a separate /mbta route, you *can* keep this,
# but then make sure you also have a mbta_form.html template.
@app.route("/mbta", methods=["GET", "POST"])
def mbta():
    if request.method == "POST":
        place = request.form.get("place", "").strip()
        stop_info = get_stop_near_place(place)
        if stop_info is None:
            return render_template(
                "result.html",
                error=f"No MBTA station found near '{place}'. Try another location.",
            )
        return render_template("result.html", stop=stop_info, place=place)

    # GET – render a dedicated form for /mbta, if you want it separated
    return render_template("mbta_form.html")


if __name__ == "__main__":
    app.run(debug=True)
