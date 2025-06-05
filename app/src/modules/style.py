import streamlit as st
import base64

def style_sidebar():
    st.markdown(
    """
    <style>
    /* Sidebar background color */
    [data-testid="stSidebar"] {
        background-color: #458bd1; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)