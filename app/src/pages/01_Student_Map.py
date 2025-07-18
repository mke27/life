import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import json
from datetime import datetime
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()
from modules.style import style_sidebar
style_sidebar()


def inv_sigmoid(value):
    """ returns the inverse sigmoid of the input. If the input is 0 or 1, rebounds the sigmoid to -3 or 3
        Args:
            value (int): value to be inversed sigmoided
        Returns:
            inv_sig (int): inverse sigmoid of input bounded between -3 and 3
    """
    if value == 1:
        value = .95
    elif value == 0:
        value = 0.05

    return np.log(value) - np.log(1-value)

API_URL = "http://web-api:4000/grace/preference"
df = pd.DataFrame()

st.markdown('''
            # Country Recommendations Map

            Set your preferences below to receive personalized country recommendations.
            Your selected reference values are relative to one another, meaning that if all sliders are set at 0, you will receive the same recommendation as setting them all at 100. To prioritise factors, the user must place it above the other factors.
            - **Education** refers to the the percentage of the population that completed tertiary education. 
            - **Health** is based on life expectancy at birth.
            - **Safety** reflects the amount of drug crimes.
            - **Environment** is measured by the country's carbon emissions.    
''')

col1, col2, col3, col4 = st.columns(4)

with col1:
    education = st.slider(
        label="Education",
        min_value=0,
        max_value=100,
        value=50,
        step=1
        )
with col2:
    health = st.slider(
        label="Health",
        min_value=0,
        max_value=100,
        value=50,
        step=1
        )
with col3:
    safety = st.slider(
        label="Safety",
        min_value=0,
        max_value=100,
        value=50,
        step=1
        )
with col4:
    environment = st.slider(
        label="Environment",
        min_value=0,
        max_value=100,
        value=50,
        step=1
        )

logger.info(f"education = {education}")
logger.info(f"health = {health}")
logger.info(f"safety = {safety}")
logger.info(f"environment = {environment}")

if st.button("Save Preferences", type="primary", use_container_width=True):

    input_vector = np.array([education, health, safety, environment])
    #st.write(f"exact input: {input_vector}")

    vector_sum = np.sum(input_vector)

    relativised_val_list = []

    #relativises
    for factor in range(len(input_vector)):
        #st.write(f"og value: {input_vector[factor]}, sum values: {vector_sum}, result: {float(input_vector[factor])/float(vector_sum)}")
        relativised_val = float(input_vector[factor])/float(vector_sum)
        relativised_val_list.append(relativised_val)

    relativised_vector = np.array([relativised_val_list[0], relativised_val_list[1], relativised_val_list[2], relativised_val_list[3]])

    #st.write(f"relativised input: {relativised_vector}")
    # inverse sigmoids
    inv_sig_input = np.array(list(map(inv_sigmoid, relativised_vector)))

    #st.write(f"invserse sigmoided input: {inv_sig_input}")

    results = requests.get(f"http://web-api:4000/model/prediction/{inv_sig_input[0]}/{inv_sig_input[1]}/{inv_sig_input[2]}/{inv_sig_input[3]}")
    results_json = json.loads(results.text)
    df = pd.DataFrame.from_dict(results_json)
    #logger.info(f"{type(results)}")
    # st.write("Status code:", results.status_code)
    # st.write(f"Response text: {results.text}, Response text type: {type(results.text)}")
    # st.write(f"Response text: {df}")

    sorted_df = df.sort_values('similarity', ascending=False)
    #st.table(df)
    fig = px.choropleth(sorted_df, title="Map of Countries That Best Match Your Priorities", scope='europe', locations='Country_input', locationmode='country names', color='similarity')
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    #st.write(sorted_df)
    # try:
    #     #JSONifying twice?
    #     json_results = results.json()  # This should be a list of dicts
    # except ValueError:
    #     st.error("Could not parse JSON from response.")
    #     st.stop()

    if results.status_code != 200:
        st.error(f"API returned error: {results.get('error', 'Unknown error')}")
        st.stop()

    try:
        country_response = requests.get("http://web-api:4000/country/country")
        country_data = country_response.json()

        country_name_to_id = {c["country_name"]: c["country_ID"] for c in country_data}

        top_country_name = sorted_df.iloc[0]["Country_input"]
        #st.write(f"top country = {top_country_name}")

        top_country_id = country_name_to_id.get(top_country_name)

        if not top_country_id:
            st.error(f"Could not find country ID for '{top_country_name}'")
            st.stop()

    except requests.exceptions.RequestException as e:
        st.error(f"Error getting country list: {str(e)}")
        st.stop()   

    pref_data = {
        "user_ID": st.session_state["user_ID"],
        "pref_date": datetime.now().isoformat(), 
        "top_country": top_country_id,
        "factorID_1": 1,
        "weight1": education,
        "factorID_2": 2,
        "weight2": health,
        "factorID_3": 3,
        "weight3": safety,
        "factorID_4": 4,
        "weight4": environment
        }
        
    #pref_dict = pd.Series.to_dict(pref_data)

    #str_data = json.dumps(pref_data)
    #json_data = json.loads(str_data)

    try:
        # Send POST request to API to save preferences
        response = requests.post(API_URL, json=pref_data)

        if response.status_code == 201:
            st.success("Preferences saved successfully!")
        else:
            err_msg = response.json().get('error', 'Unknown error')
            st.error(f"Failed to save preferences: {err_msg}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.info("Please ensure the API server is running")

if st.button('Compare Preference History', type='primary', use_container_width=True):
    st.switch_page('pages/02_Past_Prefs.py')

