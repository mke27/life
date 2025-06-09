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
# max_selected = 2

# selected_count = sum(
#     st.session_state.get(f"checkbox_{i}", False) for i in range(len(factors))
# )
current_value = True
states = list()
checkBoxColList = st.columns(4)

for i, col in enumerate(checkBoxColList):
    current_value = st.session_state.get(f"checkbox_{i}")
    with col:
        states.append(st.checkbox(
        label=factors[i],
        value=current_value,
        key= f"checkbox_{i}",
        # disabled=disabled
    ))

# for i, factor in enumerate(factors):

#     # disabled = not current_value and selected_count >= max_selected
#     states.append(st.checkbox(
#         label=factor,
#         value=current_value,
#         key=f"checkbox_{i}",
#         # disabled=disabled
#     ))

st.subheader("Most Recent News On: ")
newsColList = st.columns(3)
response = requests.get(API)
response_json = response.json()

relevant_articles = []

#[if states[article_dict['factor_id']] relevant_articles.append(article_dict) for article_dict in response_json]

# filters irrelevant articles
for article_dict in response_json:
    #st.write(article_dict)
    if states[article_dict['factor_ID']-1]:
        relevant_articles.append(article_dict)

if len(relevant_articles) != 0:
    #displays the relevant articles in the rows
    for i, article in enumerate(relevant_articles):
        with newsColList[i%len(newsColList)]:
            st.write(article)
else:
    for i, article in enumerate(response_json):
        with newsColList[i%len(newsColList)]:
            st.write(article)



#st.write(f"response={response_json}")
# with col1:
#     st.subheader("Link 1")
#     st.write("Title")
#     st.write("Author")

# with col2:
#     st.subheader("Link 2")
#     st.write("Title")
#     st.write("Author")

# with col3:
#     st.subheader("Link 3")
#     st.write("Title")
#     st.write("Author")