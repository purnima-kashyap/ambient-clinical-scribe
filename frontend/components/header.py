import streamlit as st


def show_header():

    left, right = st.columns([5, 1])

    with left:

        st.title("🩺 AI Clinical Scribe")

        st.caption(
            "Ambient Intelligence for Healthcare • AI Powered Clinical Documentation"
        )

    with right:

        st.metric(
            label="System Status",
            value="🟢 Ready"
        )

    st.divider()