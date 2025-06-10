import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.write("# About Best Life")

st.markdown(
    """
    A country’s quality of life provides important insight into the well-being of citizens and their satisfaction with the standards of living. Rather than simply relying on a single statistic to determine a country’s success, quality of life encapsulates a broader sense of how people feel about their experiences. This is typically based on several factors, and for our project we will be focusing on the following: Education, Health, Safety, Environment, and Transportation.

Our application aims to provide information and insights about and related to the quality of life in EU countries over the past 5 years. It will assist with decision making on a personal, commercial, and governmental level. A student can use this application to assess which country to attend university in by ranking their priorities, while a government official can input their country in order to identify their most lacking factor, discover the country most similar to theirs, and gain insight from recent policy implementations. Additionally, a social organization can determine the best opportunities for expansion by identifying the countries underperforming in their target focus.

The application will utilize a combination of regression and similarity scoring in order to provide valuable insights to its users. The ultimate goal is to help users understand the factors that determine their quality of life and subsequently make informed decisions through moving, policy implementation, or providing aid.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
