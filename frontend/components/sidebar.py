import streamlit as st


def show_sidebar():

    with st.sidebar:

        st.title("🩺 AI Clinical Scribe")

        st.caption("Ambient Intelligence for Healthcare")

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