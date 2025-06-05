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
st.header("University Recommendations")
st.write(
    """Select a country."""
)
country = st.selectbox("Country",
    ["Select a country", "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France",
    "Germany", "Greece", "Hungary", "Ireland", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
    "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"])

top_universities = [
            {"name": "University A", "rank": 1, "city": "City X"},
            {"name": "University B", "rank": 2, "city": "City Y"},
            {"name": "University C", "rank": 3, "city": "City Z"}
        ]

for uni in top_universities:
    key = f"show_form_{uni['name']}"
    if key not in st.session_state:
        st.session_state[key] = False

if st.button('View top universities', type='primary', use_container_width=True):
    if country == "Select a country":
        st.warning("Please select a valid country.")
    else:
        st.subheader(f"Top Universities in {country}")
        cols = st.columns(3)

        for col, uni in zip(cols, top_universities):
            with col:
                st.markdown(f"### {uni['name']}")
                st.write(f"**Rank:** {uni['rank']}")
                st.write(f"**City:** {uni['city']}")

                with st.popover("Join mailing list"):
                    st.markdown(f"Join {uni['name']}'s mailing list for more information.")
                    email = st.text_input(f"Enter your email.", key=f"email_{uni['name']}")


