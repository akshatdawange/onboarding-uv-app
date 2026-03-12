import requests
import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import time
from db import get_supabase

API_KEY = st.secrets["API_KEY"]
CITY_NAME = "Melbourne"
COUNTRY_CODE = "AU"
LIMIT = "5"

supabase = get_supabase()

response_loc = supabase.table("loc-data").select("*").execute()
rows_loc = response_loc.data

options = [f"{rows_loc['city']}, {rows_loc['country']}" for rows_loc in rows_loc]

location_map = {
    f"{row['city']}, {row['country']}": row
    for row in rows_loc
}

st.title("Sun Protection App")

CurrentLocationInformation, Statistics, PreventionMethods = st.tabs(["Current Location Information", "Statistics", "Prevention Methods"], width="stretch")

with CurrentLocationInformation:
    st.header("Current Location Information")

    st.write("Click the button below to share your location to view the UV index of your location")
    
    location = streamlit_geolocation()
    
    if location:
        lat = location["latitude"]
        lon = location["longitude"]

        # Testing block
        # st.write("Latitude:", lat)
        # st.write("Longitude:", lon)

        TIMESTAMP = int(time.time())
        Y_TIMESTAMP = TIMESTAMP - 86400

        #Testing Block
        # st.write(TIMESTAMP)
        
        if lat and lon:
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}"
            history_url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={Y_TIMESTAMP}&appid={API_KEY}"
            
            response = requests.get(url)
            response2 = requests.get(history_url)

            data = response.json()
            y_data = response2.json()

        # st.write(data)
        
            current = data["current"]
            
            temp_c = current["temp"] - 273.15
            yesterday_temp_c = y_data["data"][0]["temp"] - 273.15

            uvi = current["uvi"]
            uvi_yest = y_data["data"][0]["uvi"]

            description = current["weather"][0]["description"]

            delta_temp = temp_c - yesterday_temp_c
            delta_uvi = uvi - uvi_yest

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Current Temperature",
                f"{temp_c:.1f} °C",
                f"{delta_temp:.1f} °C vs yesterday"
            )

            col2.metric(
                "Current UVI",
                f"{uvi:.1f}",
                f"{delta_uvi:.1f} vs yesterday"

            )

    st.write("OR")

    selected = st.selectbox("Select City", options=options)

    if selected:

        lat_selc = location_map[selected]["lat"]
        lon_selc = location_map[selected]["lng"]


        if lat_selc and lon_selc:
            url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat_selc}&lon={lon_selc}&appid={API_KEY}"
            history_url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat_selc}&lon={lon_selc}&dt={Y_TIMESTAMP}&appid={API_KEY}"
            
            response = requests.get(url)
            response2 = requests.get(history_url)

            data = response.json()
            y_data = response2.json()

        # st.write(data)
        
            current = data["current"]
            
            temp_c = current["temp"] - 273.15
            yesterday_temp_c = y_data["data"][0]["temp"] - 273.15

            uvi = current["uvi"]
            uvi_yest = y_data["data"][0]["uvi"]

            description = current["weather"][0]["description"]

            delta_temp = temp_c - yesterday_temp_c
            delta_uvi = uvi - uvi_yest

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Current Temperature",
                f"{temp_c:.1f} °C",
                f"{delta_temp:.1f} °C vs yesterday"
            )

            col2.metric(
                "Current UVI",
                f"{uvi:.1f}",
                f"{delta_uvi:.1f} vs yesterday"
            )