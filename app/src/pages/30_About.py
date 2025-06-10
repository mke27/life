import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()
from modules.style import style_sidebar
style_sidebar()

st.write("# About Best Life")

st.markdown(
    """
A country's quality of life provides important insight into the well-being of citizens and their satisfaction with the standards of living. Rather than simply relying on a single statistic to determine a country's success, quality of life encapsulates a broader sense of how people feel about their experiences. This is typically based on several factors, and for our project we will be focusing on the following: Healthcare, Education, Safety, and Environment.

Our application aims to provide decision-making assistance for users looking to improve their quality of life. By utilizing data about the quality of life in EU member states, we are able to recommend countries to prospective international students, help policymakers implement new legislation, and guide activists in their expansion efforts. 

Best Life utilizes a combination of time series auto-regression and cosine similarity scoring in order to provide valuable insights to its users. The ultimate goal is to help users understand the factors that determine their quality of life and subsequently make informed decisions through moving, policy implementation, or providing aid.
    """
)

st.divider() 
st.write("# Creators")

cols = st.columns(4)

people = [
    {"photo": "assets/maya.jpeg", "name": "Max Robinson", "info": "Computer Science and Mathematics at Northeastern University"},
    {"photo": "assets/maya.jpeg", "name": "Maya Ellis", "info": "Data Science and Economics at Northeastern University"},
    {"photo": "assets/zoya.jpeg", "name": "Are Makropoulos", "info": "Computer Science at Northeastern University"},
    {"photo": "assets/zoya.jpeg", "name": "Zoya Siddiqui", "info": "Data Science and Biochemistry at Northeastern University"}
]

for col, member in zip(cols, people):
    with col:
        # Display the image (Streamlit handles sizing better here)
        st.image(member["photo"], width=100, caption=None)

        # Display the name and description
        st.markdown(f"**{member['name']}**")
        st.markdown(
            f"<p style='font-size: 0.85rem; color: #555; min-height: 80px'>{member['info']}</p>",
            unsafe_allow_html=True
        )

st.divider()

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
