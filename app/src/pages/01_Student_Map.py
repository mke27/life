import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

API_URL = "http://web-api:4000/grace/preferences"

# set the header of the page
st.header('Country Recommendations Map')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")
st.write("Set your preferences below to see the best country recommendations for you.")

df = pd.DataFrame()
fig = px.choropleth(df, scope='europe')
st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme="streamlit")

col1, col2, col3, col4 = st.columns(4)

with col1:
    education = st.slider(
        label="Education",
        min_value=0,
        max_value=100,
        value=50,
        step=1
        )
with col2:
    health = st.slider(
        label="Health",
        min_value=0,
        max_value=100,
        value=50,
        step=1
        )
with col3:
    safety = st.slider(
        label="Safety",
        min_value=0,
        max_value=100,
        value=50,
        step=1
        )
with col4:
    environment = st.slider(
        label="Environment",
        min_value=0,
        max_value=100,
        value=50,
        step=1
        )

logger.info(f"education = {education}")
logger.info(f"health = {health}")
logger.info(f"safety = {safety}")
logger.info(f"environment = {environment}")

if st.button("Save Preferences", type="primary", use_container_width=True):
    results = requests.get(f"http://web-api:4000/model/predict/{education}/{health}/{safety}/{environment}")
    #df = pd.read_json(results.text)
    logger.info(f"{type(results)}")
    st.write("Status code:", results.status_code)
    st.write(f"Response text: {results.text}, Response text type: {type(results.text)}")

    # try:
    #     #JSONifying twice?
    #     json_results = results.json()  # This should be a list of dicts
    # except ValueError:
    #     st.error("Could not parse JSON from response.")
    #     st.stop()

    if results.status_code != 200:
        st.error(f"API returned error: {results.get('error', 'Unknown error')}")
        st.stop()

    if not isinstance(results, dict):
        st.error("Unexpected response format or empty result list.")
        st.stop()

    try:
        first_result = results[0]  # first dict in the list
        top_country = first_result.get('Country_input', 'Unknown')
        similarity = first_result.get('similarity', None)
        st.write(f"Top country based on preferences: {top_country}")
        st.write(f"Similarity score: {similarity}")
    except Exception as e:
        st.error(f"Error reading prediction results: {str(e)}")
        st.write("Raw JSON:", results)
        st.stop()

    pref_data = {
        "user_ID": st.session_state['user_id'],
        "top_country": top_country,
        "factorID_1": 1,
        "weight1": education,
        "factorID_2": 2,
        "weight2": health,
        "factorID_3": 3,
        "weight3": safety,
        "factorID_4": 4,
        "weight4": environment
    }

    try:
        # Send POST request to API to save preferences
        response = requests.post(API_URL, json=pref_data)

        if response.status_code == 201:
            st.success("Preferences saved successfully!")
        else:
            err_msg = response.json().get('error', 'Unknown error')
            st.error(f"Failed to save preferences: {err_msg}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.info("Please ensure the API server is running")

if st.button('Compare Preference History', type='primary', use_container_width=True):
    st.switch_page('pages/03_Past_Prefs.py')
