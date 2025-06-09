import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

import requests

st.markdown("""
            # User Deletion

            This action is permanent and cannot be undone! The user will no longer exist.

            Please confirm you want to complete this action.

""")

if st.button("Confirm Deletion"): 
     requests.delete(f"http://web-api:4000/users/users/remove/{st.session_state['user_ID']}")
     st.switch_page('Home.py')


