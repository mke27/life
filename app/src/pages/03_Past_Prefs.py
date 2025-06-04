import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

SideBarLinks()

# add the logo
add_logo("assets/logo.png", height=400)

# set up the page
st.header("Preference History")
st.write(
    """Select 2 preference sets below to compare your recommended countries."""
)

