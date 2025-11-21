# MBTA Web App – Nearest Station & Nearby Restaurants

- This project is a Flask-based web application that allows a user to enter any location (e.g., “Fenway Park”, “Harvard Square”, “Boston Commons”), and the app returns: The nearest MBTA station, Wheelchair accessibility information,and Top 6 nearby restaurants displayed in a 3×2 grid using SerpAPI The app uses a clean styled UI with an image banner, a centered input form, and structured results. The image was obtaineed from Free Adobe Stock images

## 1. Features
### ✅ Core Requirements
- User enters a place name through an HTML form, Mapbox API converts the user’s input → latitude & longitude, MBTA API returns the nearest station and it Shows:Station Name, and Wheelchair Accessibility  

### 🔍 Error Handling
- An Empty form will displays friendly message and ask to input a Location. An Invalid location will displays an error. While No nearby stops will displays message explaining it instead of crashing  

### ⭐ Bonus Features
- The Bonus feature uses **SerpAPI Google Maps engine** to fetch top restaurants near the coordinates given, Followed by a display of restaurants in a styled **3-row × 2-column grid**  
## 2. How to Run the App
### Step 1 — Install Requirements
```
pip install -r requirements.txt
```
### Step 2 — Create a `.env` File
Inside the project folder, make a file named `.env`:
```
MAPBOX_TOKEN=your_mapbox_key_here
MBTA_API_KEY=your_mbta_key_here
SERPAPI_KEY=your_serpapi_key_here
```
These keys **must not be committed to GitHub**. So DON'T forget to place .env in a .gitignore
### Step 3 — Run the App
```
python app.py
```
or
```
flask run
```
### Step 4 — Open in Browser
```
http://127.0.0.1:5000/
```
## 3. File Structure
```
MBTA-WEB-APP-PROJECT/
│── app.py
│── mbta.py
│── README.md
│── requirements.txt
│── instructions.md
│── instructions.pdf
│── LICENSE
│── .env             (should NOT be committed publicly)
│
├── templates/
│   ├── index.html
│   └── result.html
│
└── static/
    ├── styles.css
    └── images/
        └── Boston Commons.jpeg
        └── Boston Map.jpeg
        └── Busy T.jpeg
        └── MBTA Station.jpeg (Included a few more images simply to give an opportunity to customize in the future)
```
## 4. Function Descriptions
### `Lati_Long(place)`
- Sends request to Mapbox geocoding API  
- Returns `(latitude, longitude)`  
- Raises an error if no match is found  
### `find_stop_near(lat, lon)`
- Queries MBTA API for nearest stop  
- Returns:
  - station name  
  - wheelchair accessibility  
### `get_stop_near_place(place)`
- Wrapper:
  1. Convert place → coordinates  
  2. Fetch nearest station  
### `get_nearby_restaurants(lat, lon)`
- BONUS  
- Uses SerpAPI Google Maps engine  
- Returns restaurants with:
  - name  
  - address  
  - rating  
  - phone  
## 5. HTML Templates
### index.html
- Displays the input form  
- Shows errors  
- Loads header image & CSS  
### result.html
- Shows station info  
- Shows accessibility  
- Shows 6 restaurants in a grid  
- Search Again button  
## 6. CSS Styling Overview
- Light green background  
- Emerald green form box  
- Centered layout  
- Styled restaurant cards  
- Full-width banner image  
## 7. Known Issues
- SerpAPI free tier limits  
- Mapbox may not recognize vague input  
- Visual layout may vary by screen size  
## 8. Credits
Developed by **Daniel Rodriguez**  
 
## 9. AI Usage Reflection
- Firstly, I would like to mention there was usage of AI in the project planning stage as I utilized it to come up with a outline of the neccessary steps within the project. This gave a checklist and overview of everything I must complete.In order to develop this project the usae of AI was Integral as it helped Debug issues in my data calling of API key's, found errors in my logical code that returned data, and helped integrate the data necessary for the Serpapi API data in google maps. In addition it helped understand and structure the App.py file while exploring the flask library asking questions realted to setting up the routes. In the templetes files i used AI to find materials explaning the actions i required my page to take and debug any interpretation issues I ran into while running the templates. I would like to mention,there is a heavy reliance on AI in the creation of the Style.css form as it follwed commands and logic i was completely unaware of at the start of the project. As a result AI helped breakdown each individual section and explain what they do and how it interacts with the template files.In essence the usage of AI helped plan, API calling, Logoical De-Bugging, explore the flask library, learn html formatting, and accessories the flask website using CSS and explaning the process.