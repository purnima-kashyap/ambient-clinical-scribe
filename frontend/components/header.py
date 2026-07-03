import streamlit as st

def show_header():

    col1, col2, col3, col4 = st.columns([6,2,2,2])

    with col1:
        st.title("New Consultation")

    with col2:
        st.button("🎤 Record")

    with col3:
        st.button("⬆ Upload")

    with col4:
        st.success("Processed")