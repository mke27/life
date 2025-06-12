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


SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.header('Similar Countries')
COUNTRY_API_URL = "http://web-api:4000/country/countries"
country_response = requests.get(COUNTRY_API_URL)

SCORES_API_URL = "http://web-api:4000/faye/scores_standardized"
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

if st.button(f"Find country most similar to {option}"):
    st.session_state.show_sim_country = True

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

    st.subheader(f"Most similar countries to {option}")
    st.markdown("Use the map and table to explore countries most similar in quality of life indicators.")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        fig = px.choropleth(df_renamed, title="Map of Most similar Countries",scope='europe', locations='Country', locationmode='country names', color='Similarity Score', hover_data='Similarity Score')
        st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    with col2:
        st.dataframe(df_renamed.iloc[1:][["Country", "Similarity Score"]].reset_index(drop=True), use_container_width=True, height=400)

    st.divider()
    st.subheader("Quality of Life Comparison")

    country_1 = df_renamed.iloc[0]["Country"]
    country_2 = df_renamed.iloc[1]["Country"]

    url_1 = f"http://web-api:4000/model/get_model_scores/{country_1}"
    response_1 = requests.get(url_1)
    url_2 = f"http://web-api:4000/model/get_model_scores/{country_2}"
    response_2 = requests.get(url_2)

    if response_1.status_code == 200 and response_2.status_code == 200:
        try:
            data_1 = response_1.json()
            data_2 = response_2.json()
            if isinstance(data_1, list) and isinstance(data_2, list):
                fig = plot_qol(data_1, country_1, data_2, country_2)
            else:
                st.warning("Invalid data format received from the model API.")
        except Exception as e:
            st.error(f"Error parsing model data: {str(e)}")
                    
    else:
        st.error(f"Failed to fetch QoL data for countries")



