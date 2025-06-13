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



SideBarLinks()
from modules.style import style_sidebar
style_sidebar()
add_logo("assets/logo.png", height=400)
st.markdown('''
            # Preference History

            Compare previous recommended countries. Displayed are the past preferences of education, health, safety, and environment.
''')

user_ID = st.session_state.get("user_ID", 1)

pref_response = requests.get(f"http://web-api:4000/grace/preference/{user_ID}")
if pref_response.status_code != 200:
    st.error("Failed to load user preferences.")
    st.stop()
past_prefs = pref_response.json()

country_response = requests.get("http://web-api:4000/country/country")
if country_response.status_code != 200:
    st.error("Failed to load countries.")
    st.stop()
country_data = country_response.json()
country_id_to_name = {item["country_ID"]: item["country_name"] for item in country_data}

selected_prefs = []
st.subheader("Select 2 Past Preferences")

cols = st.columns(3)
selected_prefs = []

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


for i, pref in enumerate(past_prefs):
    country_id = pref["top_country"]
    country_name = country_id_to_name.get(country_id, f"Unknown ID {country_id}")
    
    label = f"""
    {i+1}. {country_name}
    Your input:
    - Education: {pref['weight1']:.2f}
    - Health: {pref['weight2']:.2f}
    - Safety: {pref['weight3']:.2f}
    - Environment: {pref['weight4']:.2f}
    """
    col = cols[i % 3]
    if col.checkbox(label, key=f"pref_{pref['pref_ID']}"):
        selected_prefs.append(pref)

if len(selected_prefs) != 2:
    st.warning("Please select exactly 2 preferences to compare.")
else:
    if st.button("Compare Recommendations", type="primary", use_container_width=True):

        st.subheader("Comparison of Recommended Countries")
        col1, col2 = st.columns(2)
        columns = [col1, col2]

        for i, (pref, col) in enumerate(zip(selected_prefs, columns)):
            country_id = pref["top_country"]
            country = country_id_to_name.get(country_id, f"Unknown ID {country_id}")
            SCORE_URL = f"http://web-api:4000/faye/scores/{country}"
            response_scores = requests.get(SCORE_URL)
            data_scores = response_scores.json()[0]

            df = pd.DataFrame({
                    "Country": [country],
                    "Highlight": [1],
                    "Education": [data_scores["education_score"]],
                    "Health": [data_scores["health_score"]],
                    "Safety": [data_scores["safety_score"]],
                    "Environment": [data_scores["environment_score"]],
                })
 
            fig = px.choropleth(
                df,
                scope="europe",
                locations="Country",
                locationmode="country names",
                color="Highlight",
                color_continuous_scale=["lightgray", "red"],
                hover_name= "Country",
                hover_data={
                    "Country": False,
                    "Education": True,
                    "Health": True,
                    "Safety": True,
                    "Environment": True,
                    "Highlight": False  # Hide this internal field
                }
            )

            fig.update_coloraxes(showscale=False)
            fig.update_layout(title_text=f"Preference {i+1}: {country}")
            col.plotly_chart(fig, use_container_width=True)
        
        st.write("Hover over the country for more information regarding education, health, safety and environment scores. The scores represent the number of standard deviations away from the mean score the value is. A negative value indicates the factor score is below the mean while a positive value shows that the factor score is a certain amount of standard deviations above the mean.")

        country_id_1 = selected_prefs[0]["top_country"]
        country_id_2 = selected_prefs[1]["top_country"]

        country_name_1 = country_id_to_name.get(country_id_1, f"Unknown ID {country_id_1}")
        country_name_2 = country_id_to_name.get(country_id_2, f"Unknown ID {country_id_2}")

        url_1 = f"http://web-api:4000/model/model_scores/{country_name_1}"
        response_1 = requests.get(url_1)
        url_2 = f"http://web-api:4000/model/model_scores/{country_name_2}"
        response_2 = requests.get(url_2)

        if response_1.status_code == 200 and response_2.status_code == 200:
            try:
                data_1 = response_1.json()
                data_2 = response_2.json()
                if isinstance(data_1, list) and isinstance(data_2, list):
                    st.markdown('''
                                ## Quality of Life Comparison
                                
                                Compares the historical and predicted happiness scores of the countries. 
                                The scores for each country evaluate their citizens quality of life on a 0 (worst possible life) to 10 (best possible life) scale.
                    ''')
                    fig = plot_qol(data_1, country_name_1, data_2, country_name_2)
                else:
                    st.warning("Invalid data format received from the model API.")
            except Exception as e:
                st.error(f"Error parsing model data: {str(e)}")
                    
        else:
            st.error(f"Failed to fetch QoL data for countries")

            

