import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
import requests

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

# add the logo
add_logo("assets/logo.png", height=400)

# set up the page
st.header("University Recommendations")
st.write("""Select a country.""")

# Fetch list of countries
response = requests.get("http://web-api:4000/country/country")
data = response.json()
country_name_to_id = {item["country_name"]: item["country_ID"] for item in data}
country_names = list(country_name_to_id.keys())

# Country dropdown
country = st.selectbox("Country", options=["Select a country"] + country_names)

# Handle button click to view universities
if st.button('View top universities', type='primary', use_container_width=True):
    if country == "Select a country":
        st.warning("Please select a valid country.")
    else:
        country_id = country_name_to_id[country]

        # Fetch universities from API
        try:
            uni_response = requests.get(f"http://web-api:4000/grace/university/{country_id}")
            universities = uni_response.json()

            if "error" in universities:
                st.warning(universities["error"])
            elif not universities:
                st.info(f"No universities found in {country}.")
            else:
                st.subheader(f"Top Universities in {country}")
                cols = st.columns(3)

                for i, uni in enumerate(universities):
                    col = cols[i % 3]
                    with col:
                        st.markdown(f"### {uni['university_name']}")
                        st.write(f"**Website:** [{uni['uni_url']}]({uni['uni_url']})")

                        with st.popover("Join mailing list"):
                            st.markdown(f"Join {uni['university_name']}'s mailing list for more information.")
                            email = st.text_input("Enter your email.", key=f"email_{uni['university_ID']}")

        except Exception as e:
            st.error(f"Failed to fetch universities: {e}")



