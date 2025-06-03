import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Activst, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Map of Expansion Recommendations', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Expansion_Map.py')

if st.button('View QoL Change Over Time', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_QoL_Change.py')

if st.button('View Current Organizations', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Current_Orgs.py')
