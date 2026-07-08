import os
import streamlit as st

from components.sidebar import show_sidebar
from components.header import show_header
from components.upload import show_upload
from components.transcript import show_transcript
from components.soap import show_soap
from components.icd import show_icd

st.set_page_config(
    page_title="AI Clinical Scribe",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
css_path = os.path.join(os.path.dirname(__file__), "style.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

show_sidebar()

show_header()

col1, col2 = st.columns([1, 2])

with col1:
    show_upload()

with col2:
    show_transcript()

col3, col4 = st.columns([1.4, 1])

with col3:
    show_soap()

with col4:
    show_icd()