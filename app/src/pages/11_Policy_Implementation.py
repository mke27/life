import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')
SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

API = 'http://web-api:4000/james/policy'

st.title('Policy News')

st.subheader("View recent EU policy news related to: ")

#change to be more dynamic later -- with get factors
factors = ["Education", "Health", "Safety", "Environment"]
factor_to_id = {factor: i+1 for i, factor in enumerate(factors)}
selected_factors = st.multiselect(
    "Filter by topic:",
    options=factors,
    default=factors
)

selected_ids = [factor_to_id[factor] for factor in selected_factors]

response = requests.get(API)
if response.status_code != 200:
    st.error("Failed to fetch data from the API.")
    st.stop()
response_json = response.json()

filtered_articles = [
    article for article in response_json if article['factor_ID'] in selected_ids
]

st.write("### Most Recent News")

newsColList = st.columns(3)
if not filtered_articles:
    st.warning("No articles found for the selected topics.")
else:
    for i, article in enumerate(filtered_articles):
        with newsColList[i % len(newsColList)]:
            with st.container(border=True):
                st.markdown(f"**{article['title']}**")
                st.markdown(f"[Read full article]({article['urls']})", unsafe_allow_html=True)
                st.write(f"Published on: {article['date_created']}")
                st.write(f"Topic: {factors[article['factor_ID']-1]}")


#current_value = True
#states = list()
#checkBoxColList = st.columns(4)

#for i, col in enumerate(checkBoxColList):
    #current_value = st.session_state.get(f"checkbox_{i}")
    #with col:
        #states.append(st.checkbox(
        #label=factors[i],
        #value=current_value,
        #key= f"checkbox_{i}",
        # disabled=disabled
    #))

# for i, factor in enumerate(factors):

#     # disabled = not current_value and selected_count >= max_selected
#     states.append(st.checkbox(
#         label=factor,
#         value=current_value,
#         key=f"checkbox_{i}",
#         # disabled=disabled
#     ))

#st.subheader("Most Recent News On: ")
#newsColList = st.columns(3)
#response = requests.get(API)
#response_json = response.json()

#relevant_articles = []

#[if states[article_dict['factor_id']] relevant_articles.append(article_dict) for article_dict in response_json]

# filters irrelevant articles
#for article_dict in response_json:
    #st.write(article_dict)
    #if states[article_dict['factor_ID']-1]:
        #relevant_articles.append(article_dict)

#if len(relevant_articles) != 0:
    #displays the relevant articles in the rows
    #for i, article in enumerate(relevant_articles):
        #with newsColList[i%len(newsColList)]:
            #st.subheader(article['title'])
            #st.write(article['urls'])
            #st.write(article['date_created'])
#else:
    #for i, article in enumerate(response_json):
        #with newsColList[i%len(newsColList)]:
            #st.subheader(article['title'])
            #st.write(article['urls'])
            #st.write(article['date_created'])
