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

education = st.slider(
    label="Education",
    min_value=0,
    max_value=100,
    value=50,
    step=1
    )
health = st.slider(
    label="Health",
    min_value=0,
    max_value=100,
    value=50,
    step=1
    )
safety = st.slider(
    label="Safety",
    min_value=0,
    max_value=100,
    value=50,
    step=1
    )
transportation = st.slider(
    label="Transportation",
    min_value=0,
    max_value=100,
    value=50,
    step=1
    )
environment = st.slider(
    label="Environment",
    min_value=0,
    max_value=100,
    value=50,
    step=1
    )

prefs = [education, health, safety, transportation, environment]

df = pd.DataFrame()
fig = px.choropleth(df, scope='europe')
st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme="streamlit")

#if st.button('Save Preferences', 
             #type='primary',
             #use_container_width=True):
  # save prefs to database?
