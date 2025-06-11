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



SideBarLinks()
from modules.style import style_sidebar
style_sidebar()
add_logo("assets/logo.png", height=400)
st.header("Preference History")
st.write("Select 2 preference sets below to compare your recommended countries.")

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
            df = pd.DataFrame({"Country": [country], "Highlight": [1]})
            fig = px.choropleth(
                df,
                scope="europe",
                locations="Country",
                locationmode="country names",
                color="Highlight",
                color_continuous_scale=["lightgray", "red"]
            )
            fig.update_coloraxes(showscale=False)
            fig.update_layout(title_text=f"Preference {i+1}: {country}")
            col.plotly_chart(fig, use_container_width=True)

            st.subheader(f"{country} Scores")
            qol_url = f"http://web-api:4000/model/get_model_scores/{country}"
            qol_response = requests.get(qol_url)
            if qol_response.status_code == 200:
                try:
                    qol_data = qol_response.json()
                    if isinstance(qol_data, list) and len(qol_data) > 0:
                        plot_qol(qol_data, country)
                    else:
                        st.warning(f"No QoL data available for {country}.")
                except Exception as e:
                    st.error(f"Error parsing QoL data for {country}: {str(e)}")
                    st.text(f"Raw response: {qol_response.text}")
                
            else:
                st.error(f"Failed to fetch QoL data for {country}. Status code: {qol_response.status_code}")
                st.text(f"Response: {qol_response.text}")
            

