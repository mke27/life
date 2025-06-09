import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
import requests
from modules.nav import SideBarLinks
import plotly.express as px
import matplotlib.pyplot as plt


SideBarLinks()
from modules.style import style_sidebar
style_sidebar()
add_logo("assets/logo.png", height=400)
st.header("Preference History")
st.write("Select 2 preference sets below to compare your recommended countries.")

user_ID = st.session_state.get("user_ID", 1)

pref_response = requests.get(f"http://web-api:4000/grace/preference/{user_ID}")
if pref_response.status_code != 200:
    st.error("Failed to load user preferences.")
    st.stop()
past_prefs = pref_response.json()

country_response = requests.get("http://web-api:4000/country/country")
if country_response.status_code != 200:
    st.error("Failed to load countries.")
    st.stop()
country_data = country_response.json()
country_id_to_name = {item["country_ID"]: item["country_name"] for item in country_data}

selected_prefs = []
st.subheader("Select 2 Past Preferences")

cols = st.columns(5)
for i, pref in enumerate(past_prefs):
    country_id = pref["top_country"]
    country_name = country_id_to_name.get(country_id, f"Unknown ID {country_id}")
    label = f"{i+1}. {country_name}, Education: {pref['weight1']}, Health: {pref['weight2']}, Safety: {pref['weight3']}, Environment: {pref['weight4']}"
    if cols[i].checkbox(label, key=f"pref_{pref['pref_ID']}"):
        selected_prefs.append(pref)

if len(selected_prefs) != 2:
    st.warning("Please select exactly 2 preferences to compare.")
else:
    if st.button("Compare Recommendations", type="primary", use_container_width=True):
        selected_country_names = [
            country_id_to_name.get(pref["top_country"], "Unknown Country")
            for pref in selected_prefs
        ]

        st.subheader("Comparison of Recommended Countries")
        col1, col2 = st.columns(2)

        for i, col in enumerate([col1, col2]):
            country = selected_country_names[i]
            df = pd.DataFrame({"Country": [country], "Highlight": [1]})
            fig = px.choropleth(
                df,
                scope="europe",
                locations="Country",
                locationmode="country names",
                color="Highlight",
                color_continuous_scale=["lightgray", "red"]
            )
            fig.update_coloraxes(showscale=False)
            fig.update_layout(title_text=f"Preference {i+1}: {country}")
            col.plotly_chart(fig, use_container_width=True)
