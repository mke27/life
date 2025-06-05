import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
import requests
from modules.nav import SideBarLinks

SideBarLinks()
add_logo("assets/logo.png", height=400)
st.header("Preference History")
st.write("Select 2 preference sets below to compare your recommended countries.")

# Dummy preference list
past_prefs = ["Run 1", "Run 2", "Run 3", "Run 4", "Run 5"]

# Let user select 2 preferences
selected = []
for i, label in enumerate(past_prefs):
    if st.checkbox(label, key=f"checkbox_{i}"):
        selected.append(i + 1)  # assuming pref_ID starts from 1

if len(selected) != 2:
    st.warning("Please select exactly 2 preference sets to compare.")
else:
    if st.button("Compare Recommendations", type="primary", use_container_width=True):
        top_countries = []
        for pref_id in selected:
            response = requests.get(f"http://web-api:4000/grace/preferences/{pref_id}/top_country")
            if response.status_code == 200:
                try:
                    country = list(response.json().values())[0]  # Get first value
                    top_countries.append(country)
                except Exception as e:
                    st.error(f"Error parsing top country for pref_ID {pref_id}: {str(e)}")
            else:
                st.error(f"API error for pref_ID {pref_id}: {response.status_code}")

        # Coordinates dictionary (simplified)
        country_coords = {
            "Austria": [13.3333, 47.3333],
            "Belgium": [4.4699, 50.5039],
            "France": [2.2137, 46.2276],
            "Germany": [10.4515, 51.1657],
            "Spain": [-3.7492, 40.4637],
            # Add more as needed
        }

        # Check both countries exist in mapping
        if len(top_countries) == 2 and all(c in country_coords for c in top_countries):
            col1, col2 = st.columns(2)

            for idx, col in enumerate([col1, col2]):
                country = top_countries[idx]
                lat, lon = country_coords[country]
                view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=4)

                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=pd.DataFrame([[lon, lat]], columns=["lon", "lat"]),
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=100000,
                )

                col.subheader(f"Top Country: {country}")
                col.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
                                          initial_view_state=view_state,
                                          layers=[layer]))
        else:
            st.error("One or both selected countries are missing from the coordinates map.")
