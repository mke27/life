import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.title('View Existing Organizations')

st.write(
    """Select a country."""
)

response = requests.get("http://web-api:4000/country/country")
data = response.json()
country_name_to_id = {item["country_name"]: item["country_ID"] for item in data}

factor_response = requests.get("http://web-api:4000/country/factor")
data = factor_response.json()
factor_name_to_id = {item["factor_name"]: item["factor_ID"] for item in data}

country = st.selectbox("Country", ["Select a country"] + list(country_name_to_id.keys()))
factor = st.selectbox("Factors", ["Select a factor"] + list(factor_name_to_id.keys()))

if st.button('Submit', type='primary', use_container_width=True):
    if country == "Select a country" or factor == "Select a factor":
        st.warning("Please select a valid country and factor.")
    else:
        country_ID = country_name_to_id[country]
        factor_ID = factor_name_to_id[factor]

        st.subheader(f"Existing organizations focused on {factor} in {country}")
        try:
            results = requests.get(f"http://web-api:4000/faye/orgs/{country_ID}/{factor_ID}")
            json_results = results.json()

            if "error" in json_results:
                st.warning(json_results["error"])
            else:
                cols = st.columns(3)
                for col, org in zip(cols, json_results):
                    with col:
                        st.markdown(f"### {org['org_name']}")
                        org_url = org.get('org_url')
                        if org_url: 
                            st.write(f"**Link:** {org_url}")

        except Exception as e:
            st.error(f"Failed to fetch data: {e}")
