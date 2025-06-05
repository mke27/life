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

past_prefs = ["Run 1", "Run 2", "Run 3", "Run 4", "Run 5"]

selected_count = sum(
    st.session_state.get(f"checkbox_{i}", False) for i in range(len(past_prefs)))

max_selected = 2

for i, factor in enumerate(past_prefs):
    current_value = st.session_state.get(f"checkbox_{i}", False)
    disabled = not current_value and selected_count >= max_selected
    state = st.checkbox(
        label=factor, 
        value=current_value, 
        key=f"checkbox_{i}",
        disabled=disabled
    )

if st.button('View QoL Comparison Chart', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_QoL_Chart.py')

