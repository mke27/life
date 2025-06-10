import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

import requests


UPDATE_FIRSTNAME = "http://web-api:4000/users/update/first-name"
UPDATE_USERNAME = "http://web-api:4000/users/update/username"
st.title("Edit Profile")
st.write("Please fill out this form to change your first name or username.")
with st.form(key = "form"):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input(label = "Change first name:", max_chars = 20, placeholder = st.session_state['first_name'])

    with col2:
        user_name = st.text_input(label = "Change username:", max_chars = 20, placeholder = st.session_state['user_name'])

    submit_button = st.form_submit_button(label="Update Profile")

    if submit_button:
        if not first_name and not user_name:
            st.error("No first name or username entered.")
        else:
            if first_name:
                if first_name != st.session_state['first_name']:
                    try:
                        response = requests.put(UPDATE_FIRSTNAME, json={
                            "first_name": first_name,
                            "user_ID": st.session_state['user_ID']})
                        if response.status_code == 200:
                            st.session_state['first_name'] = first_name
                            st.success(f"Updated first name to: {first_name}")
                        else:
                            st.error(f"Failed to change first name: {response.json().get('error', 'Unknown error')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to the API: {str(e)}")
                        st.info("Please ensure the API server is running")
                else:
                    st.error("Same first name entered.")

            if user_name:
                if user_name != st.session_state['user_name']:
                    try:
                        response = requests.put(UPDATE_USERNAME, json={
                            "user_name": user_name,
                            "user_ID": st.session_state['user_ID']})
                        if response.status_code == 200:
                            st.session_state['user_name'] = user_name
                            st.success(f"Updated username to: {user_name}")
                        else:
                            st.error(f"Failed to change username: {response.json().get('error', 'Unknown error')}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to the API: {str(e)}")
                        st.info("Please ensure the API server is running")
                else:
                    st.error("Same username entered.")

        

st.write("")

if st.button("Delete Profile"):
     st.switch_page("pages/33_Remove_User.py")
     # requests.delete(f"http://web-api:4000/users/users/remove/{user_ID}")


