import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.DataFrame()

fig = px.choropleth(df, locations='iso_alpha', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'unemp':'unemployment rate'}
                          )

st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")