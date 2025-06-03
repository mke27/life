import streamlit as st
import pandas as pd
import plotly.express as px
from modules.nav import SideBarLinks

df = pd.DataFrame()

fig = px.choropleth(df, scope='europe')

SideBarLinks()

st.set_page_config(layout = 'wide')

st.title("Map Of Europe")

st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme="streamlit")

st.radio("Feautures", options=['Health', 'Education', 'Environment', 'Safety', 'Transport'], 
         index=0, horizontal=True, label_visibility="visible",)