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
st.markdown('''
            # Expansion Map

            The map demonstrates countries on a gradient scale that are deeply affected by each factor. Lighter blue areas indicate lower scores, highlighting greater needs and opportunities for improvement in health, education, environment, or safety.
            ''')
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
            f"http://web-api:4000/faye/scores_standardized")
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

fig = px.choropleth(df_renamed, scope='europe', locations='Country', locationmode='country names', color=input_name, color_continuous_scale='Blues_r')
st.plotly_chart(fig, use_container_width=True, theme="streamlit")

st.dataframe(df_renamed.iloc[1:].reset_index(drop=True), use_container_width=True, height=400, hide_index=True)
st.caption("""
The scores shown in the above table are standardised. This means that for the factor, we take all the previous values for that factor and find the mean and standard deviation. We then subtract the mean from the real value and divide by the standard deviation to get the standardised score. This score can be understood as the number of standard deviations away from the mean score this value is. For example, a score of -0.5 means that the real value is 0.5 standard deviations below the mean.
""")
#fig = px.choropleth(df, scope='europe', color='similarity', locations = 'Country_input', locationmode='country names')

#st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme="streamlit")