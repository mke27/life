import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.title(f"Welcome Prospective University Student, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Country Recommendations', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Student_Map.py')

if st.button('View University Recommendations', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/03_University_Recs.py')