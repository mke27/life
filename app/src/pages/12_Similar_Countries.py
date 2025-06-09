import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.header('Similar Countries')
COUNTRY_API_URL = "http://web-api:4000/country/countries"
country_response = requests.get(COUNTRY_API_URL)

MODEL_API_URL = "http://web-api:4000/faye/scores"
scores_response = requests.get(MODEL_API_URL)

if(country_response.status_code == 200):
    countries = country_response.json()

st.subheader("Choose Country")

option = st.selectbox(
    label = "",
    options=countries
)

if "show_sim_country" not in st.session_state:
    st.session_state.show_sim_country = False

if "prev_country" not in st.session_state or st.session_state.prev_country != option:
    st.session_state.show_sim_country = False
    st.session_state.prev_country = option

if st.button(f"Country most similar to {option}:"):
    st.session_state.show_sim_country = True
    
if st.session_state.show_sim_country:
    #get the most similar country based on country --- route
    model_response_json = scores_response.json()

    # df = pd.DataFrame.from_dict(model_response_json)
    # df['environment_score'] = -df['environment_score']
    # df['safety_score'] = -df['safety_score']

    # compare_to = df[]

    # df_sorted = df.sort_values(input_issue, ascending=True)
    st.write('Belgium')
