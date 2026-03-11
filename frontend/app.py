import sys
import os
import streamlit as st

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from frontend import login
from frontend.pages import dashboard

st.set_page_config(page_title="ICFA", page_icon="📊", layout="wide")

# Hide default Streamlit pages navigation
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Initialise session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "token" not in st.session_state:
    st.session_state.token = ""


if not st.session_state.logged_in:
    login.show()
else:
    dashboard.show()
