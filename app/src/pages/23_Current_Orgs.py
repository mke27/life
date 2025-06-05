import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('View Existing Organizations')

st.write(
    """Select a country."""
)
country = st.selectbox("Country",
    ["Select a country", "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia", "Finland", "France",
    "Germany", "Greece", "Hungary", "Ireland", "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
    "Poland", "Portugal", "Romania", "Slovakia", "Slovenia", "Spain", "Sweden"])

st.write(
    """Select a factor."""
)
factor = st.selectbox("Factors",
    ["Select a factor", "healthcare", "education", "environment", "safety"])

current_orgs = [
            {"name": "Organization A", "link": "URL X"},
            {"name": "Organization B", "link": "URL Y"},
            {"name": "Organization C", "link": "URL Z"}
        ]

if st.button('Submit', type='primary', use_container_width=True):
    if country == "Select a country":
        st.warning("Please select a valid country.")
    if country == "Select a factor":
        st.warning("Please select a valid factor.")
    else:
        st.subheader(f"Existing organizations focused on {factor} in {country}")
        cols = st.columns(3)

        for col, uni in zip(cols, current_orgs):
            with col:
                st.markdown(f"### {uni['name']}")
                st.write(f"**Link:** {uni['link']}")





