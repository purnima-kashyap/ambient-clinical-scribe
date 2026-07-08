import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def show_upload():

    st.subheader("🎤 Upload Consultation")

    st.caption(
        "Upload a doctor-patient consultation recording to generate a transcript, SOAP note, and ICD-10 recommendations."
    )

    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["wav", "mp3", "m4a"],
        help="Supported formats: WAV, MP3, M4A"
    )

    if uploaded_file:

        st.audio(uploaded_file)

        st.success(f"Selected file: **{uploaded_file.name}**")

        if st.button(
            "🩺 Generate Clinical Report",
            use_container_width=True
        ):

            with st.spinner("Generating clinical report..."):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                try:
                    response = requests.post(
                        f"{API_URL}/transcribe",
                        files=files
                    )

                except requests.exceptions.ConnectionError:
                    st.error("Backend server is not running.")
                    st.stop()

            if response.status_code == 200:

                st.success("✅ Clinical report generated successfully.")

                st.session_state.transcript = response.json()["segments"]

            else:

                st.error(response.text)