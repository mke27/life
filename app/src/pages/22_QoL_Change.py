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
import plotly.graph_objects as go

st.set_page_config(layout = 'wide')

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.markdown('''
            # Quality of Life Comparison

            Choose two countries to compare their historical and predicted happiness scores. The scores for each country evaluate their citizens quality of life on a 0 (worst possible life) to 10 (best possible life) scale.
            ''')

def plot_qol(qol_data, country, qol_data2 = None, country2 = None):
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

    qol_df = pd.DataFrame(qol_data)
    qol_df["Source"] = qol_df["year"].apply(
        lambda y: "Historical Score" if y in historical_years else (
            "Predicted Score" if y in predicted_years else "Unknown"
        )
    )

    fig.add_trace(go.Scatter(
        x=qol_df['year'],
        y=qol_df['qol_score'],
        mode='lines+markers',
        name=f'{country} QoL',
        line=dict(color='royalblue'),
        customdata=qol_df[["Source"]],
        hovertemplate=
            f'<b>{country}</b><br>' +
            'Year: %{x}<br>' +
            'QoL Score: %{y:.3f}<br>' +
            'Type: %{customdata[0]}<extra></extra>'
    ))

    if qol_data2 is not None and country2 is not None:
        qol_df2 = pd.DataFrame(qol_data2)
        qol_df2["Source"] = qol_df2["year"].apply(
            lambda y: "Historical Score" if y in historical_years else (
                "Predicted Score" if y in predicted_years else "Unknown"
            )
        )

        fig.add_trace(go.Scatter(
            x=qol_df2['year'],
            y=qol_df2['qol_score'],
            mode='lines+markers',
            name=f'{country2} QoL',
            line=dict(color='crimson'),
            customdata=qol_df2[["Source"]],
            hovertemplate=
                f'<b>{country2}</b><br>' +
                'Year: %{x}<br>' +
                'QoL Score: %{y:.3f}<br>' +
                'Type: %{customdata[0]}<extra></extra>'
        ))

    fig.add_vline(x=2022.5, line_width=2, line_dash="dash", line_color="gray")

    fig.add_vrect(
        x0=2023, x1=max(
            qol_df['year'].max(),
            qol_df2['year'].max() if qol_data2 else 2027
        ),
        fillcolor="lightgray", opacity=0.3,
        layer="below", line_width=0,
        annotation_text="Predicted", annotation_position="top left"
    )

    fig.update_layout(
        title="Quality of Life (Historical and Projected)",
        xaxis_title="Year",
        yaxis_title="Quality of Life Score"
    )

    st.plotly_chart(fig, use_container_width=True, key=f"qol_chart_{country}")


COUNTRY_API_URL = "http://web-api:4000/country/countries"
country_response = requests.get(COUNTRY_API_URL)
if(country_response.status_code == 200):
    countries = country_response.json()

if "compare" not in st.session_state:
    st.session_state.compare = False
if "country_1" not in st.session_state:
    st.session_state.country_1 = countries[0] if countries else ""
if "country_2" not in st.session_state:
    st.session_state.country_2 = countries[1] if len(countries) > 1 else ""

def activate_compare():
    if st.session_state.country_1 == st.session_state.country_2:
        st.warning("Please select two different countries.")
    else:
        st.session_state.compare = True

def reset():
    st.session_state.compare = False

if not st.session_state.compare:
    col1, col2 = st.columns(2)
    with col1:
        country_1 = st.selectbox("Select First Country", options=countries, key="country_1")
    with col2:
        country_2 = st.selectbox("Select Second Country", options=countries, key="country_2")
    st.button("Compare QoL Scores", on_click=activate_compare)

else:
    country_1 = st.session_state.country_1
    country_2 = st.session_state.country_2
    url_1 = f"http://web-api:4000/model/get_model_scores/{country_1}"
    url_2 = f"http://web-api:4000/model/get_model_scores/{country_2}"
    response_1 = requests.get(url_1)
    response_2 = requests.get(url_2)
    if response_1.status_code == 200 and response_2.status_code == 200:
        try:
            data_1 = response_1.json()
            data_2 = response_2.json()

            if isinstance(data_1, list) and isinstance(data_2, list):
                st.subheader(f"{country_1} vs. {country_2}")
                plot_qol(data_1, country_1, data_2, country_2)
            else:
                st.error("Invalid data received from the API.")
        except Exception as e:
            st.error(f"Error parsing data: {str(e)}")
    else:
        st.error(f"Failed to fetch QoL data.")
    
    st.button("Select New Countries", on_click=reset)


