import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')
SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.title('Policy News')


st.subheader("View recent EU policy news related to: ")

#change to be more dynamic later -- with get factors
factors = ["Education", "Health", "Safety", "Environment"]
max_selected = 2

selected_count = sum(
    st.session_state.get(f"checkbox_{i}", False) for i in range(len(factors))
)

for i, factor in enumerate(factors):
    current_value = st.session_state.get(f"checkbox_{i}", False)
    disabled = not current_value and selected_count >= max_selected
    state = st.checkbox(
        label=factor,
        value=current_value,
        key=f"checkbox_{i}",
        disabled=disabled
    )

if st.button('View Policies'):
    st.subheader("Most Recent News On: ")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Link 1")
        st.write("Title")
        st.write("Author")

    with col2:
        st.subheader("Link 2")
        st.write("Title")
        st.write("Author")

    with col3:
        st.subheader("Link 3")
        st.write("Title")
        st.write("Author")