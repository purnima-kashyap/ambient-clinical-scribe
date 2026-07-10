import streamlit as st


def show_sidebar():

    with st.sidebar:

        st.markdown(
        "<h2 style='color:#1f2937;'>🩺 AI Clinical Scribe</h2>",
        unsafe_allow_html=True
        )

        st.markdown(
        "<p style='color:#6b7280; font-size:14px;'>Ambient Intelligence for Healthcare</p>",
        unsafe_allow_html=True
        )

        st.divider()

        st.markdown("### 🏠 Dashboard")

        st.button(
            "📝 New Consultation",
            use_container_width=True
        )

        st.button(
            "👥 Patients",
            use_container_width=True
        )

        st.button(
            "📄 SOAP Notes",
            use_container_width=True
        )

        st.button(
            "💊 ICD-10 Codes",
            use_container_width=True
        )

        st.button(
            "🕒 History",
            use_container_width=True
        )

        st.button(
            "⚙️ Settings",
            use_container_width=True
        )

        st.divider()

        st.button(
            "🚪 Logout",
            use_container_width=True
        )