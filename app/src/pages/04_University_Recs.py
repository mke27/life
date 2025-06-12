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

add_logo("assets/logo.png", height=400)

st.header("University Recommendations")
st.write("""Select a country.""")

response = requests.get("http://web-api:4000/country/country")
data = response.json()
country_name_to_id = {item["country_name"]: item["country_ID"] for item in data}
country_names = list(country_name_to_id.keys())

# Get current user ID — make sure this exists in session_state
user_ID = st.session_state.get("user_ID", "default_user")

# Initialize user_data dict if missing
if "user_data" not in st.session_state:
    st.session_state["user_data"] = {}

# Initialize this user's dict if missing or wrong type
if user_ID not in st.session_state["user_data"] or not isinstance(st.session_state["user_data"][user_ID], dict):
    st.session_state["user_data"][user_ID] = {}

user_data = st.session_state["user_data"][user_ID]

country = st.selectbox("Country", options=["Select a country"] + country_names)

if st.button('View top universities', type='primary', use_container_width=True):
    if country != "Select a country":
        user_data["selected_country"] = country
    else:
        st.warning("Please select a valid country.")

# Check for selected_country inside this user's data
if "selected_country" in user_data:
    country = user_data["selected_country"]
    country_id = country_name_to_id[country]
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
                    st.markdown(
                        f"""
                        <div style="border:1px solid #ccc; border-radius:10px; padding:15px; margin:5px; background-color:#f9f9f9;">
                            <h4 style='margin-bottom:5px'>{uni['university_name']}</h4>
                            <p><a href="{uni['uni_url']}" target="_blank">Visit Website</a></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    button_key = f"subscribe_{uni['university_ID']}"
                    email_key = f"{user_ID}_email_{uni['university_ID']}"
                    success_key = f"{user_ID}_subscribed_{uni['university_ID']}"
                    with st.popover("Join mailing list"):
                        with st.form(key=f"form_{uni['university_ID']}"):
                            st.markdown(f"Join {uni['university_name']}'s mailing list for more information.")
                            email = st.text_input(label="Enter your email", label_visibility="collapsed", key=email_key)
                            submitted = st.form_submit_button("Subscribe")
                            if submitted:
                                st.session_state[success_key] = True
                        if st.session_state.get(success_key, False):
                            st.success(f"Subscribed to {uni['university_name']}!")
    except Exception as e:
        st.error(f"Failed to fetch universities: {e}")

st.caption("*University rankings sourced from [mastersportal.com](https://www.mastersportal.com)*")
