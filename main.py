import streamlit as st
import streamlit_js_eval as steval
from urllib.request import urlopen
import json
import os

url = "https://maps.googleapis.com/maps/api/geocode/json?"
googleAPIKey = os.getenv("googleMapsAPIKey")

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

st.title("Weather Forecast")
try:
    location = st.text_input("Location:", key="locationInput", value=accurateLocation)
except NameError:
    location = st.text_input("Location:", key="locationInput")

days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select number of days to be forecast")
option = st.selectbox("Select data to view", ("Temperature", "Weather"))

try:
    subText = (f"{option} for the next 24 hours in {location}") if days == 1 else (f"{option} for the next {days} days in {location}")
except TypeError:
    subText = ""

st.header(subText, divider="rainbow")