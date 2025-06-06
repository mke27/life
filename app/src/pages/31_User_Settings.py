import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

import requests

st.write("# User Settings")

username = st.session_state['username']
user_id = st.session_state['user_id']
st.write(f"### Change username from {username}")

st.write(f"Current user_id: {user_id}")

UPDATE_USERNAME = "http://web-api:4000/users/users/name"
DELETE_USER = "http://web-api:4000/users/users/remove/{user_id}"

update_username = st.text_input(
    label = "Please enter new username",
    max_chars = 20,
    placeholder = "Username here"
)
if update_username:
    try:
        response = requests.put(UPDATE_USERNAME, json={
             "user_name":update_username,
             "user_id": user_id})
        if response.status_code == 200:
            st.session_state['username'] = update_username
            st.success(f"Updated username to: {update_username}")
        else:
            st.error(
                        f"Failed to change username: {response.json().get('error', 'Unknown error')}"
                    )
    
    except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

st.write("")
st.markdown("""
            ### Delete user
            Warning: This action is permanent. 
            It will delete this username from users and take you back to the home page.
            """)

if st.button("Delete user"):
     st.switch_page('Home.py')
     requests.delete(DELETE_USER)