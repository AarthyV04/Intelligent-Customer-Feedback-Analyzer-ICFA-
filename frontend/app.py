import sys
import os

from frontend import login

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import streamlit as st

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

from frontend.pages import dashboard

if not st.session_state.logged_in:
    login.show()
else:
    dashboard.show()
