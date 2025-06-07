import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

import requests

st.write("# User Settings")

user_name = st.session_state['user_name']
user_id = st.session_state['user_id']
first_name = st.session_state['first_name']
user_role = st.session_state['role']
st.markdown(f"""
            ### About User
            First Name: {first_name}

            Username: {user_name}

            User ID: {user_id}

            Role: {user_role}

            ### Update first name:
""")

UPDATE_FIRSTNAME = "http://web-api:4000/users/update/first-name"

update_firstname = st.text_input(
      label = "Please enter new first name",
      max_chars = 20,
      placeholder = "Username here"
)
if update_firstname:
    try:
        response = requests.put(UPDATE_FIRSTNAME, json={
              "first_name": update_firstname,
              "user_id": user_id})
        if response.status_code == 200:
            st.session_state['first_name'] = update_firstname
            st.success(f"Updated first name to: {update_firstname}")
        else:
            st.error(f"Failed to change first name: {response.json().get('error', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {str(e)}")
        st.info("Please ensure the API server is running")

UPDATE_USERNAME = "http://web-api:4000/users/update/username"

st.write("### Update username:")
update_username = st.text_input(
    label = "Please enter new username",
    max_chars = 20,
    placeholder = "Username here"
)
if update_username:
    try:
        response = requests.put(UPDATE_USERNAME, json={
             "user_name": update_username,
             "user_id": user_id})
        if response.status_code == 200:
            st.session_state['user_name'] = update_username
            st.success(f"Updated username to: {update_username}")
        else:
            st.error(f"Failed to change username: {response.json().get('error', 'Unknown error')}")
    
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
     requests.delete(f"http://web-api:4000/users/users/remove/{user_id}")
     st.switch_page('Home.py')