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

education = st.slider(
    label="Education",
    min_value=0,
    max_value=100,
    value=50,
    step=1
    )
st.write(education)
