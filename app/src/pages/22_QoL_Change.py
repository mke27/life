import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.title('Quality of Life')

st.write('\n\n')
st.write('## Coming Soon!')

