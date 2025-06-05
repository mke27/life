import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')
SideBarLinks()

st.title('Similar Country and Policy Implementation')
col1, col2 = st.columns(2)

API_URL = "http://web-api:4000/life/countries"
response = requests.get(API_URL)
if(response.status_code == 200):
    countries = response.json()

with col1:
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
        if st.button('Belgium', 
             type='primary',
             use_container_width=True):
            st.switch_page('pages/17_Sim_Country_Graph.py')


    st.subheader("View recent EU policy related to: ")

    #change to be more dynamic later -- with get factors
    factors = ["Education", "Health", "Safety", "Environment"]
    max_selected = 2

    selected_count = sum(
        st.session_state.get(f"checkbox_{i}", False) for i in range(len(factors))
    )

    for i, factor in enumerate(factors):
        current_value = st.session_state.get(f"checkbox_{i}", False)
        disabled = not current_value and selected_count >= max_selected
        state = st.checkbox(
            label=factor,
            value=current_value,
            key=f"checkbox_{i}",
            disabled=disabled
        )

    st.button('View Policies')


with col2:
    st.subheader("Most Recent News From the EU Commission about ")

