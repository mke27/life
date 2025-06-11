import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import json
import pandas as pd
import numpy as np
import plotly.express as px

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.header('Similar Countries')
COUNTRY_API_URL = "http://web-api:4000/country/countries"
country_response = requests.get(COUNTRY_API_URL)

SCORES_API_URL = "http://web-api:4000/faye/scores"
scores_response = requests.get(SCORES_API_URL)

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

    score_results_json = json.loads(scores_response.text)
    df_scores = pd.DataFrame.from_dict(score_results_json)
    #st.write(df_scores)
    #st.write(df_scores[df_scores.country_name == option])

    selected_row = df_scores[df_scores.country_name == option]

    comparison_vector = np.array([selected_row['education_score'], selected_row['health_score'],
                                  selected_row['safety_score'], selected_row['environment_score']])
    #st.write(comparison_vector)
    model_results = requests.get(
        f"http://web-api:4000/model/predict/{comparison_vector[0][0]}/{comparison_vector[1][0]}/{comparison_vector[2][0]}/{comparison_vector[3][0]}")
    #st.write(model_results.text)
    results_json = json.loads(model_results.text)
    df_similarites = pd.DataFrame.from_dict(results_json)

    df_sorted = df_similarites.sort_values('similarity', ascending = False)

    df_renamed = df_sorted.rename(columns={'Country_input':'Country', 'similarity':'Similarity Score'})

    fig = px.choropleth(df_renamed, title="Map of Most similar Countries",scope='europe', locations='Country', locationmode='country names', color='Similarity Score', hover_data='Similarity Score')
    st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme="streamlit")

    st.write(df_renamed.iloc[1:,:])

