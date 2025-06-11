import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
import logging
import json
logger = logging.getLogger(__name__)
from modules.nav import SideBarLinks


SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

struggle = st.radio("Select the feature you would like to tackle", options=['Health', 'Education', 'Environment', 'Safety'], 
         index=0, horizontal=True, label_visibility="visible")

match struggle:
    case 'Health':
        input_issue = 'health_score'
        input_name = 'Health Score'
    case 'Education':
        input_issue = 'education_score'
        input_name = 'Education Score'
    case 'Environment':
        input_issue = 'environment_score'
        input_name = 'Environment Score'
    case 'Safety':
        input_issue = 'safety_score'
        input_name = 'Safety Score'
    case _:
        input_issue = 'health_score'
        input_name = 'Health Score'

results = requests.get(
            f"http://web-api:4000/faye/scores")
results_json = json.loads(results.text)
df = pd.DataFrame.from_dict(results_json)
df['environment_score'] = -df['environment_score']
df['safety_score'] = -df['safety_score']
df_sorted = df.sort_values(input_issue, ascending=True)

df_renamed = df_sorted.rename(columns={'country_name': 'Country',
                                       'environment_score': 'Environment Score', 
                                       'safety_score': 'Safety Score', 
                                       'health_score': 'Health Score', 
                                       'education_score':'Education Score'})

fig = px.choropleth(df_renamed, scope='europe', locations='Country', locationmode='country names', color=input_name)
st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme="streamlit")

st.write(df_renamed)
#fig = px.choropleth(df, scope='europe', color='similarity', locations = 'Country_input', locationmode='country names')

#st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme="streamlit")