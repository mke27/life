import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.title(f"Welcome Activist, {st.session_state['username']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Map of Expansion Recommendations', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Faye_map_for_concerns.py')

if st.button('View QoL Change Over Time', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_QoL_Change.py')

if st.button('View Current Organizations', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Current_Orgs.py')
