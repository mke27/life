import streamlit as st
import time
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

import requests

st.markdown("""
            # Profile Deletion

            This action is permanent and cannot be undone! The profile will no longer exist.

            Please confirm you want to complete this action.

""")

if st.button("Confirm Deletion"): 
     status_text = st.empty()
     deletion_bar = st.progress(0)
     for i in range(100):
          time.sleep(0.03)
          deletion_bar.progress(i)
          status_text.text("Deleting Profile...")

     requests.delete(f"http://web-api:4000/users/user/{st.session_state['user_ID']}")
     st.switch_page('Home.py')


