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
import plotly.graph_objects as go
import json

st.set_page_config(layout = 'wide')

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.title('Quality of Life Change Over Time')

COUNTRY_API_URL = "http://web-api:4000/country/countries"
country_response = requests.get(COUNTRY_API_URL)

if(country_response.status_code == 200):
    countries = country_response.json()

with st.form("country_form"):
    option = st.selectbox("Select a country:", countries)
    submitted = st.form_submit_button("Submit")

def plot_qol(qol_data, country):
    """
    Plots actual and predicted QoL scores over time for a single country
    
    Args:
        - qol_data: list of dicts with keys 'year' and 'qol_score'
        - country: Name of the country (str)
    """  
    historical_years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    predicted_years = [2023, 2024, 2025, 2026, 2027]

    qol_df = pd.DataFrame(qol_data)

    qol_df["Projected?"] = "Unknown"  

    qol_df.loc[qol_df["year"].isin(historical_years), "Projected?"] = "Historical Score"
    qol_df.loc[qol_df["year"].isin(predicted_years), "Projected?"] = "Predicted Score"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=qol_df['year'],
        y=qol_df['qol_score'],
        mode='lines+markers',
        name='QoL Score',
        line=dict(color='royalblue'),
        customdata=qol_df[['Projected?']], 
        hovertemplate=
            'Year: %{x}<br>' +
            'QoL Score: %{y:.3f}<br>' +
            'Projected?: %{customdata[0]}<extra></extra>'
    ))

    fig.add_vline(x=2022.5, line_width=2, line_dash="dash", line_color="gray")

    fig.add_vrect(
        x0=2023, x1=qol_df['year'].max(),
        fillcolor="lightgray", opacity=0.3,
        layer="below", line_width=0,
        annotation_text="Predicted", annotation_position="top left"
    )

    fig.update_layout(
        title= f"Quality of Life (Historical and Projected) for {country}",
        xaxis_title="Year",
        yaxis_title="Quality of Life Score",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True, key=f"qol_chart_{country}")

if submitted:
    # Plot QoL
    MODEL_API_URL = f"http://web-api:4000/model/get_model_scores/{option}"
    qol_response = requests.get(MODEL_API_URL)

    if qol_response.status_code == 200:
        qol_data = qol_response.json()
        plot_qol(qol_data, option)
    else:
        st.error(f"Could not fetch QoL data for {option}.")

    # Fetch and display 2022 factor scores
    results = requests.get(
            f"http://web-api:4000/faye/scores")
    results_json = json.loads(results.text)
    df = pd.DataFrame.from_dict(results_json)
    df['environment_score'] = -df['environment_score']
    df['safety_score'] = -df['safety_score']

    df_renamed = df.rename(columns={'country_name': 'Country',
                                        'environment_score': 'Environment Score', 
                                        'safety_score': 'Safety Score', 
                                        'health_score': 'Health Score', 
                                        'education_score':'Education Score'})

    df_filtered = df_renamed[df_renamed['Country'] == option]
    df_filtered = df_filtered.reset_index(drop=True)
    df_filtered = df_filtered.loc[:, ~df_filtered.columns.str.contains('^Unnamed|index')]

    if not df_filtered.empty:
        st.subheader(f"Factor Scores for {option} (2022)")
        st.table(df_filtered)
    else:
        st.warning(f"No factor score data found for {option}.")

st.caption("*Education = Percent in tertiary education, Health = Life expectancy at birth, Safety = Drug crimes, Environment = Carbon emissions, QoL = World Happiness Index Scores*")

