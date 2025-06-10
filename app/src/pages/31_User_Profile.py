import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

import requests

st.write("# My Profile")

st.info(f"""
            ### About User
            First Name: {st.session_state['first_name']}

            Username: {st.session_state['user_name']}

            User ID: {st.session_state['user_ID']}

            Role: {st.session_state['role']}
"""
)
if st.button("Edit Profile", type="primary"):
    st.switch_page("pages/32_User_Edit.py")