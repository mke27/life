import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Country Recommendations Map')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")
st.write("Set your preferences below to see the best country recommendations for you.")

df = pd.DataFrame()
fig = px.choropleth(df, scope='europe')
st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme="streamlit")

col1, col2, col3, col4, col5 = st.columns(5)

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
    transportation = st.slider(
        label="Transportation",
        min_value=0,
        max_value=100,
        value=50,
        step=1
        )
with col5:
    environment = st.slider(
        label="Environment",
        min_value=0,
        max_value=100,
        value=50,
        step=1
        )

prefs = [education, health, safety, transportation, environment]


if st.button('Save Preferences', type='primary', use_container_width=True):
    preferences = {
        "Education": education,
        "Health": health,
        "Safety": safety,
        "Transportation": transportation,
        "Environment": environment
    }

if st.button('Compare Preference History', type='primary', use_container_width=True):
    st.switch_page('pages/03_Past_Prefs.py')
