import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
import logging
logger = logging.getLogger(__name__)
from modules.nav import SideBarLinks


SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.title("Map Of Europe")


struggle = st.radio("Feautures", options=['Health', 'Education', 'Environment', 'Safety'], 
         index=0, horizontal=True, label_visibility="visible")

#logger.info(f"selection {struggle}")
match struggle:
    case 'Health':
        input_issue = np.array([0,100,100,100])
    case 'Education':
        input_issue = np.array([100,0,100,100])
    case 'Environment':
        input_issue = np.array([100,100,0,100])
    case 'Safety':
        input_issue = np.array([100,100,100,0])
    case _:
        input_issue = np.array([0,100,100,100])

results = requests.get(
            f"http://web-api:4000/model/predict/{input_issue[0]}/{input_issue[1]}/{input_issue[2]}/{input_issue[3]}")
#logger.info(f"result: {results}")
st.write(results.text)
#logger.info(df)

fig = px.choropleth(results, scope='europe')

st.plotly_chart(fig, use_container_width=True, sharing="streamlit", theme="streamlit")