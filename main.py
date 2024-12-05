import streamlit as st
import streamlit_js_eval as steval
from urllib.request import urlopen
import json
import os
import plotly.express as px
from functions import getData
from datetime import datetime

url = "https://maps.googleapis.com/maps/api/geocode/json?"
googleAPIKey = os.getenv("googleMapsAPIKey")
weatherAPIKey = os.getenv("weatherAPIKey")

# Return users current location
currentLocation = steval.get_geolocation()

try:
    currentLatitude = currentLocation["coords"]["latitude"]
    currentLongitude = currentLocation["coords"]["longitude"]
    url += "latlng=%s,%s&sensor=false&key=%s" % (currentLatitude, currentLongitude, googleAPIKey)
    v = urlopen(url).read()
    j = json.loads(v)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']
        if "locality" in c['types']:
            locality = c['long_name']
    accurateLocation = f"{locality}, {town}, {country}"
except TypeError:
    pass

# Add title and other widgets
st.title("Weather Forecast")
try:
    location = st.text_input("Location:", key="locationInput", value=accurateLocation, placeholder="Enter location")
except NameError:
    location = st.text_input("Location:", key="locationInput", placeholder="Enter location")

days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select number of days to be forecast")
option = st.selectbox("Select data to view", ("Temperature", "Weather"))

subText = (f"{option} for the next 24 hours in {location}") if days == 1 else (f"{option} for the next {days} days in {location}")

st.header(subText, divider="rainbow")

if location:
    filteredData = getData(weatherAPIKey, location, days)

    if option == "Temperature":
        # Create temp plot
        temperatures = [dict["data"]["realTemp"] for dict in filteredData] # returns all temperature data
        dates = [dict["dateTime"] for dict in filteredData] # gets all dates
        figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (°C)"})
        st.plotly_chart(figure)
    elif option == "Weather":
        # Create weather diagram
        images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png", "Rain": "images/rain.png", "Snow": "images/snow.png"}
        date = ""
        for item in filteredData:
            if item["date"] != date: # only create subheader once for each date
                date = item["date"]
                formattedDate = datetime.strptime(date, "%Y-%m-%d").strftime("%A %d %B %Y")
                st.subheader(formattedDate, divider=True)
                cols = st.columns(8)
            
            st.text(item["data"]["time"])
            st.image(images[item["data"]["weather"]], width=100)